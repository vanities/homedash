from server import app as application

if __name__ == "__main__":
	# secret key used for debugging in console/debugger
    application.secret_key = urandom(12)
    application.run()