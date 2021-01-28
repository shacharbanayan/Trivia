# Protocol Constants
CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"who_is_logged_msg" : "LOGGED",
"get_question_msg" : "GET_QUESTION",
"send_answer_msg" : "SEND_ANSWER",
"my_score_msg" : "MY_SCORE",
"get_highest_score_msg" : "HIGHSCORE"
}


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"error_msg" : "ERROR",
"who_is_logged_ans" : "LOGGED_ANSWER",
"get_question_msg" : "YOUR_QUESTION",
"correct_ans_msg" : "CORRECT_ANSWER",
"wrong_ans_msg" : "WRONG_ANSWER",
"my_score_ans" : "YOUR_SCORE",
"get_highest_score_ans" : "ALL_SCORE",
"no_questions_msg" : "NO_QUESTIONS"
}


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	# """
	# Gets command name (str) and data field (str) and creates a valid protocol message
	# Returns: str, or None if error occured
	# """
	full_msg = ""
	if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
		return ERROR_RETURN
	extantion_length = CMD_FIELD_LENGTH - len(cmd)
	data_length = len(data)
	length = (4-len(str(data_length))) * '0' + str(data_length)
	return cmd + (" " * extantion_length) + DELIMITER + length +DELIMITER + data


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	splitted_data = data.split(DELIMITER, 2)
	if len(splitted_data) != 3 :
		# print(1)
		return None, None
	cmd = splitted_data[0].strip()
	if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
		print(cmd)
		return None, None
	if len(splitted_data[1]) != 4:
		# print(3)
		return None, None
	try:
		length = int(splitted_data[1])
	except:
		# print(4)
		return None, None
	msg = splitted_data[2]
	if len(msg) != length:
		# print(5)
		return None, None
	return cmd, msg

	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	splitted_massage = msg.split(DATA_DELIMITER)
	if len(splitted_massage) != expected_fields:
		return ERROR_RETURN
	return splitted_massage


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	if len(msg_fields != 3):
		return ERROR_RETURN
	command = msg_fields[0]
	length = msg_fields[1]
	massage = msg_fields[2]
	extantion_length = CMD_FIELD_LENGTH - len(command)
	full_msg = command + (" " * extantion_length) + DELIMITER + str(length) + DELIMITER + massage
	return full_msg