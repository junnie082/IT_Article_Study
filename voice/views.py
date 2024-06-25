import os
from django.utils import timezone

import pyaudio
import wave
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, resolve_url, render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from openai import OpenAI

from attendance.function.attendance import update_attendance
from ias.function.cmpStrings import chkErrors, cmp_input_article, cal_hit
from ias.models import AI, Input

# Load environment variables
load_dotenv()

# Set up OpenAI API key
API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Define constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

# Global variable to track interruption status
interrupted = False


# Function to print device information
def print_device_info():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(
            f"Device {i}: {info['name']}, Max Input Channels: {info['maxInputChannels']}, Max Output Channels: {info['maxOutputChannels']}")
    p.terminate()


# Print device information to determine the supported number of channels
print_device_info()


def find_device_index(p, device_name):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if device_name in info.get('name'):
            return i
    return None


@csrf_exempt
def transcribe_audio(request, ai_id):
    print('transcribe_audio')
    ai = get_object_or_404(AI, pk=ai_id)
    # Record audio from the client-side
    frames = record_audio()
    if frames is None:
        return JsonResponse({'status': 'error', 'message': 'Recording device not found or other error occurred'})

    # Transcribe the recorded audio to text
    text_result = speech_to_text(frames)
    text_result = str(text_result)
    print('text_result: ' + text_result)

    if request.method == 'POST':
        print('Form is valid')  # Check if the form is valid
        input = Input.objects.create(
            author=request.user,
            create_date=timezone.now(),
            content=text_result,
            ai=ai,
            errCheckedStr=' '.join(chkErrors(text_result, ai.engContent)[0]),
        )
        input.errCheckedStr = chkErrors(input.content, ai.engContent.replace('-', ' '))
        input.isTheSame = cmp_input_article(input.content, ai.engContent)
        input.hit = cal_hit(input)

        update_attendance(input)
        print('input.errCheckstr: ' + str(input.errCheckedStr))
        input.save()
        return redirect('{}#input_{}'.format(
            resolve_url('ias:ai_detail', ai_id=ai.id), input.id
        ))
    else:
        print('Received non-POST request')  # Print if request method is not 'POST'
        return HttpResponseNotAllowed(['POST'])  # Return HTTP 405 Method Not Allowed for non-POST requests


@csrf_exempt
def interrupt(request):
    global interrupted
    interrupted = True
    print('Recording interrupted!')
    return JsonResponse({'status': 'success', 'message': 'Recording interrupted'})


def record_audio():
    print('Recording audio...')

    # Reset the interrupted flag
    global interrupted
    interrupted = False

    # Initialize PyAudio instance
    audio = pyaudio.PyAudio()

    # Find the device index for the desired input device
    device_name = "외장 마이크"  # Replace with the name of your input device
    device_index = find_device_index(audio, device_name)

    if device_index is None:
        print(f"Input device '{device_name}' not found.")
        audio.terminate()
        return None

    # Open the stream using the specified input device
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK,
                        input_device_index=device_index)
    frames = []

    # Check for interruption while recording
    while not interrupted:
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording and clean up resources
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print('Recording stopped.')

    # Save recorded audio to WAV file
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        os.remove(WAVE_OUTPUT_FILENAME)

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return frames


def speech_to_text(frames):
    # Open the recorded audio file
    audio_file = open(WAVE_OUTPUT_FILENAME, "rb")

    # Perform transcription using OpenAI API
    response = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

    # Extract the transcribed words from the response
    wordlist = response.words

    # Extract only the 'word' values from the list of dictionaries
    words = [word['word'] for word in wordlist]
    words = ' '.join(words)

    print('words: ' + str(words))

    return words
