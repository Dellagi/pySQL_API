from prompt_toolkit.validation import Validator, ValidationError
import re


class userValidator(Validator):
	def validate(self, document):
		ok = re.match('^[a-zA-Z]+[a-zA-Z0-9]+[_]?[a-zA-Z0-9]+$', document.text)
		if not ok:
			raise ValidationError(
				message='Please enter a valid email address',
				cursor_position=len(document.text))  # Move cursor to end

