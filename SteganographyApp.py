# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Significant Bit (LSB) encoding.

from PIL import Image

def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    msgLength = len(msg)
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msgLength, green, blue)  # Store message length in red channel

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            greenBinary = greenBinary[0:7] + letterBinary[0]
            blueBinary = blueBinary[0:7] + letterBinary[1]

        elif pixel % 3 == 1:
            redBinary = redBinary[0:7] + letterBinary[2]
            greenBinary = greenBinary[0:7] + letterBinary[3]
            blueBinary = blueBinary[0:7] + letterBinary[4]

        else:
            redBinary = redBinary[0:7] + letterBinary[5]
            greenBinary = greenBinary[0:7] + letterBinary[6]
            blueBinary = blueBinary[0:7] + letterBinary[7]
            letterSpot += 1

        red = binaryToNumber(redBinary)
        green = binaryToNumber(greenBinary)
        blue = binaryToNumber(blueBinary)

        pixels[x, y] = (red, green, blue)
        pixel += 1

    img.save("secretImg.png", 'PNG')
    print("Message encoded and saved as secretImg.png")

def decode(img):
    msg = ""
    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red  # Length was stored here during encoding

    width, height = img.size
    letterBinary = ""
    pixel = 0

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]
        elif pixel % 3 == 1:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
        else:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
            letterAscii = binaryToNumber(letterBinary)
            msg += chr(letterAscii)

        pixel += 1

    return msg

# Helper functions

def numberToBinary(num):
    """Converts a base10 number (0-255) to an 8-bit binary string."""
    return format(num, '08b')

def binaryToNumber(bin_str):
    """Converts an 8-bit binary string to a base10 number."""
    return int(bin_str, 2)

def main():
    # ENCODE
    myImg = Image.open('pki.png')  # Use a PNG image
    myMsg = "This is a secret message I will hide in an image."
    encode(myImg, myMsg)
    myImg.close()

    # DECODE
    yourImg = Image.open('secretImg.png')
    msg = decode(yourImg)
    yourImg.close()
    print("Decoded message:", msg)

if __name__ == '__main__':
    main()
