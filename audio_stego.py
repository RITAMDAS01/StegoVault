import wave

def hide_in_audio(audio_path, secret_msg, output_path):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    
    # Append dummy data to message to mark end
    secret_msg = secret_msg + "###END###"
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secret_msg])))
    
    # Replace LSB of audio frames
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
        
    frame_modified = bytes(frame_bytes)
    
    newAudio = wave.open(output_path, 'wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified)
    newAudio.close()
    audio.close()
    return output_path

def reveal_from_audio(audio_path):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    
    extracted = ""
    for i in range(len(frame_bytes)):
        extracted += str(frame_bytes[i] & 1)

    # Convert binary to text
    chars = []
    for i in range(0, len(extracted), 8):
        byte = extracted[i:i+8]
        chars.append(chr(int(byte, 2)))
        # Check for end marker
        if chars[-1] == '#' and ''.join(chars[-9:]) == "###END###":
            return ''.join(chars[:-9])
            
    return "No message found (or too long)."