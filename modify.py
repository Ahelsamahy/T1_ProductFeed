import xml.etree.ElementTree as ET

mytree = ET.parse('Input.xml')
myroot = mytree.getroot()
dataRecord = myroot.findall("DATA_RECORD")
recordLen = len(dataRecord)
counterPos = 0

uniqueId = []


def addElement(whatToAdd, underWhat, value):
    for allElem in myroot.findall('DATA_RECORD'):
        underIt = allElem.find(underWhat)
        new_tag = ET.Element(whatToAdd)
        new_tag.text = value
        new_tag.tail = underIt.tail
        index = list(allElem).index(underIt)
        allElem.insert(index+1, new_tag)


addElement("additional_image_link", "image_link", " ")
addElement("availability", "additional_image_link", "in_stock")
addElement("condition", "brand", "new")


for index in range(0, recordLen):
    myroot[index][3].text = str(
        "https://butopea.com/p/" + myroot[index][3].text)
    myroot[index][4].text = str(
        "https://butopea.com/" + myroot[index][4].text)
    if len(myroot[index][5].text) > 2:
        myroot[index][5].text = str(
            "https://butopea.com/" + myroot[index][5].text)
    myroot[index][7].text = str(
        myroot[index][7].text + " HUF")


# move the <image_link> text to the <additional_image_link> if id are the same with the ones after it.
for index in range(0, recordLen):
    counter = 1
    if counter+index < recordLen:
        while (myroot[index][1].text == myroot[index+counter][1].text):
            myroot[index][5].text = myroot[index][5].text + \
                "\n" + myroot[index+counter][4].text
            myroot[index+counter][4].text = " "
            counter += 1
# delete parent element if subelement <image_link> is empty
for target in myroot.findall('DATA_RECORD'):
    f_list = [t.text for t in target.findall('./image_link')]
    if " " in f_list:
        myroot.remove(target)


# make sure there are unique IDs only [from Google Merchant product data specifications]
duplicatedIDs = []
for IDS in myroot.iter('id'):
    if IDS.text in uniqueId:
        duplicatedIDs.append(IDS.text)
    else:
        uniqueId.append(IDS.text)
        counterPos += 1
for IDS in duplicatedIDs:
    print("the ID", IDS, "is duplicated")

print("checked IDS for", counterPos, "product")


def checkFormat():
    print("checking format ... \n")

    for index in range(0, len(uniqueId)):
        if (len(myroot[index][0].text) > 50):
            print("Max is 50 character, please reduce this id [" +
                  myroot[index][0].text+"] and try again")

        if (len(myroot[index][1].text) > 150):
            print("Max is 150 character, please reduce this title \n[" +
                  myroot[index][1].text+"] and try again")

        if (len(myroot[index][2].text) > 5000):
            print("Max is 5000 character, please reduce this description \n[" +
                  myroot[index][2].text+"] and try again")
        elif ("free shipping" in myroot[index][2].text):
            print("Can't use 'free shipping' in description, will remove it")
            myroot[index][2].text.replace("free shipping", " ")

        additionalImageList = myroot[index][5].text.split("\n")
        for elm in additionalImageList:
            if (len(elm) > 2000):
                print("Max is 2000 character, please reduce the additional image link of \n[" +
                      elm+"]and try again \n")
                
        if (len(myroot[index][8].text) > 70):
            print("Max is 70 character, please reduce the length of brand \n[" +
                  myroot[index][8].text+"] and try again")


checkFormat()
mytree.write('feed.xml')
