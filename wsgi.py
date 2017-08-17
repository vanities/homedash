from server import app as application

	# secret key used for debugging in console/debugger
    application.secret_key = urandom(12)
if __name__ == "__main__":
    application.run()
