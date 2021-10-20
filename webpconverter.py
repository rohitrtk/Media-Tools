import os

# https://pypi.org/project/webptools/
# pip install webptools
from webptools import grant_permission
from webptools import cwebp
from webptools import dwebp

DEFAULT_QUALITY = 80
DEFAULT_IMG_EXT = 'jpg'

def clamp(value: int, minValue: int=0, maxValue: int=100) -> int:
	"""
	Returns an integer clamped between the minimum and maximum values.
	>>> clamp(50)
	50
	>>> clamp(5, minValue=10)
	5
	"""
	return max(minValue, min(value, maxValue))

def _cwebp(input: str, output: str, quality: int) -> None:
	"""
	Runs the cwebp function and displays its output to console.
	"""
	print(cwebp(input_image=input, output_image=output, option='-q {0}'.format(quality), logging='-v'))

def _dwebp(input: str, output: str) -> None:
	"""
	Runs the dwebp function and displays its output to console.
	"""
	print(dwebp(input_image=input, output_image=output, option='-o', logging='-v'))

def begin_encode() -> None:
	"""
	Begins the encoding process from w/e file type to webp.
	"""
	input_path = input('Please specify the file or directory to convert to webp.\n')
	quality 	 = input('Please specify an image quality between 0 and 100, or leave blank to use the default of 80.\n')
	if quality:
		try:
			quality = clamp(int(quality))
		except ValueError:
			print('Unable to read input. Using default of 80!')
			quality = DEFAULT_QUALITY
	else:
		quality = DEFAULT_QUALITY

	# Number of files that have been encoded
	encoded = 0

	# Handle file
	if os.path.isfile(input_path):
		file_name, file_ext = os.path.splitext(input_path)
		output_path = file_name + '.webp'
		_cwebp(input_path, output_path, quality)
		encoded += 1
	
	# Handle directory
	elif os.path.isdir(input_path):
		# Allow the user to enter multiple image types
		img_types = input('Please specify image types. If there are multiple types, please space seperate them. You can leave this blank to use the default of \'jpg\'.\n').split()
		if len(img_types) == 0:
			img_types = [DEFAULT_IMG_EXT]
		
		# For each file in the given directory...
		for f in os.listdir(input_path):
			f = os.path.join(input_path, f)
			file_name, file_ext = os.path.splitext(f)
			file_ext = file_ext[1:].lower()

			# If the object we're looking at is a file and it's one of the image types specified...
			if os.path.isfile(f) and file_ext in img_types:
				output_path = file_name + '.webp'
				_cwebp(f, output_path, quality)
				encoded += 1

	print('Succesfully encoded {0} files.'.format(encoded))

def begin_decode():
	"""
	Begins the decoding process from webp to the specified file type.
	"""
	input_path = input('Please specify the file or directory to convert from webp.\n')
	output_ext = input('Please specify the output file extension (jpg, png, etc...) or leave blank to use the default of \'jpg\'.\n')
	
	# If output extension is blank, use default of jpg
	if not output_ext:
		output_ext = DEFAULT_IMG_EXT

	# Number of files decoded
	decoded = 0

	# Handle file
	if os.path.isfile(input_path):
		file_name, file_ext = os.path.splitext(input_path)
		if file_ext != '.webp':
			print('The file you specified is not a webp file!')
			return
		output_path = file_name + '.' + output_ext
		_dwebp(input_path, output_path)
		decoded += 1

	# Handle directory
	elif os.path.isdir(input_path):
		# For each file in the given directory...
		for f in os.listdir(input_path):
			f = os.path.join(input_path, f)
			file_name, file_ext = os.path.splitext(f)
			
			# If the object we're looking at is a file and it's one of the image types specified...
			if os.path.isfile(f) and file_ext == '.webp':
				output_path = file_name + '.' + output_ext
				_dwebp(f, output_path)
				decoded += 1

	print('Succesfully decoded {0} files.'.format(decoded))

# Main check
if __name__ == '__main__':
	grant_permission()

	_input = int(input('Enter 1 to encode an image to webp.\nEnter 2 to decode an image from webp.\n'))
	
	if _input == 1:
		begin_encode()
	elif _input == 2:
		begin_decode()
	else:
		print('Unrecognized input.')
