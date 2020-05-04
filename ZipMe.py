import os

path = r"C:\Users\Justin\PycharmProjects\PlaceRequestLambdaFunction"
zip = path + ".zip"


def zipAll():
    os.system("del {}".format(zip))
    command = "7z a -tzip {} ".format(zip)
    for child in os.listdir(path):
        childpath = os.path.join(path, child)
        command += childpath + " "
    os.system(command)

def upload():
    command = "aws lambda update-function-code --function-name GooglePlacesRequest --zip-file fileb://{}".format(zip)
    os.system(command)


if __name__=="__main__":
    zipAll()
    upload()