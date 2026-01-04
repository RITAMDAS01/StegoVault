from stegano import lsb

def hide_in_image(image_path, secret_message, output_path):
    # LSB Steganography
    secret = lsb.hide(image_path, secret_message)
    secret.save(output_path)
    return output_path

def reveal_from_image(image_path):
    try:
        clear_message = lsb.reveal(image_path)
        return clear_message
    except:
        return "No hidden data or corrupted file."