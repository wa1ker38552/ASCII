from PIL import Image
import requests


def ascii(url, ratio, dump='ascii.txt', size=2, option=3, invert=False):
  options = [
    ['█', '▓', '▒', '░', ' '],
    list('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`''. '),
    list('@%#*+=-:. ')
  ]
  if invert is True:
    chars = options[option-1][::-1]
  else:
    chars = options[option-1]
  
  with open('image.png', 'wb') as file:
    request = requests.get(url)
    file.write(request.content)

  im = Image.open('image.png')
  width, height = im.size
  im.resize((round(width/ratio), round(height/ratio))).save('image.png')

  im = Image.open('image.png')
  width, height = im.size
  pixels = []
  pix = im.load()

  for y in range(height):
    line = []
    for x in range(width):
      line.append(pix[x, y])
    pixels.append(line)

  image = []
  for line in pixels:
    l = []
    for pixel in line:
      # convert to luminance
      luminance = 0.2126*pixel[0] + 0.7152*pixel[1] + 0.0722*pixel[2]

      x = 0
      for char in chars:
        if round(luminance) in range(x, x+round(255/len(chars))):
          l.append(char*size)
          break
        x += round(255/len(chars))
        
    image.append(''.join(l))

  with open(dump, 'w') as file:
    file.write('\n'.join(image))

url = 'https://cdn.britannica.com/62/85162-050-C8698F1F/CN-Tower-Toronto.jpg'
ascii(url, 30, option=2, invert=False)
