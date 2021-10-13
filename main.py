import os

# https://pypi.org/project/webptools/
# pip install webptools
from webptools import grant_permission
from webptools import cwebp
from webptools import dwebp

# Clamps an integer between a minimum value and a maximum value
def clamp(value, minValue=0, maxValue=100):
	return max(minValue, min(value, maxValue))

def _cwebp(input, output, quality):
	print(cwebp(input_image=input, output_image=output, option='-q {0}'.format(quality), logging='-v'))

# Begins the encoding process from w/e file type to .webp
def begin_encode():
	input_path 	= input('Please specify the file or directory to convert to webp.\n')
	quality 		= clamp(int(input('Please specify an image quality (typically 80).\n')))

	encoded = 0

	if os.path.isfile(input_path):
		# Handle file
		output_path = input_path.split('.')[0] + '.webp'
		_cwebp(input_path, output_path, quality)
		encoded += 1
	elif os.path.isdir(input_path):
		# Handle directory
		img_types = input('Please specify image types. If there are multiple types, please space seperate them.\n').split()
		for f in os.listdir(input_path):
			f = os.path.join(input_path, f)
			file_split = f.split('.')
			if os.path.isfile(f) and file_split[1] in img_types:
				output_path = file_split[0] + '.webp'
				_cwebp(f, output_path, quality)
				encoded += 1

	print('Succesfully encoded {0} files.'.format(encoded))

# Begins the decoding process from .webp to a specified file type
def begin_decode():
	raise NotImplementedError

# Main check
if __name__ == '__main__':
	grant_permission()

	_input = int(input('Enter 1 to encode an image to webp.\nEnter 2 to decode an image from webp.\n'))
	
	if _input == 1:
		begin_encode()
	elif _input == 2:
		begin_decode()
	else:
		print('Unrecognized input. Please try again.')	
	

