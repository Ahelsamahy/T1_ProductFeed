import xml.etree.ElementTree as ET

mytree = ET.parse('Input.xml')
myroot = mytree.getroot()
dataRecord = myroot.findall("DATA_RECORD")
recordLen = len(myroot.findall('DATA_RECORD'))
counterPos = 0
counterNeg = 0

uniqueId = []

# add empty additional_image_link element
for allElem in myroot.findall('DATA_RECORD'):
    underIt = allElem.find('image_link')
    new_tag = ET.Element('additional_image_link')
    new_tag.text = " "
    new_tag.tail = underIt.tail
    index = list(allElem).index(underIt)
    allElem.insert(index+1, new_tag)

for index in range(0, recordLen):
    myroot[index][4].text = str(
        "https://butopea.com/p/" + myroot[index][4].text)
    if len(myroot[index][5].text) > 2:
        myroot[index][5].text = str(
            "https://butopea.com/p/" + myroot[index][5].text)


# move the image link to the additional_image_link element if id are the same with the ones after it.
for index in range(0, recordLen):
    counter = 1
    if counter+index < recordLen:
        while (myroot[index][1].text == myroot[index+counter][1].text):
            myroot[index][5].text = myroot[index][5].text + \
                " \n " + myroot[index+counter][4].text
            myroot[index+counter][4].text = " "
            counter += 1
    for target in myroot:
        f_list= [t.text for t in target.findall('.//image_link')]
        if " " in f_list:
            myroot.remove(target)
    recordLen = len(myroot.findall('DATA_RECORD'))


# for allElem in myroot.findall('DATA_RECORD'):
#     underIt = allElem.find('id')
#     counterPos+=1
#     new_tag = ET.Element('uniqueID')
#     new_tag.text =str(counterPos)
#     new_tag.tail = underIt.tail

#     index = list(allElem).index(underIt)
#     allElem.insert(index+1, new_tag)


# for IDS in myroot.iter('id'):
#     if IDS.text in uniqueId:
#       # print("max is 50 character, please reduce the id and try again")

#       counterNeg+=1
#     else:
#       uniqueId.append(IDS.text)
#       IDS.text = str("https://butopea.com/p/"+(IDS.text))
#       counterPos += 1
# print("there are ",counterNeg, "who have same id with other products")
# print("checked IDS for",counterPos, "product")
# counter = 0


# for links in myroot.iter('link'):
#     if (links.text>50):
#       print("max is 50 character, please reduce the id and try again")
#     else:
#       links.text = str("https://butopea.com/p/"+(links.text))
#       counter += 1
# print("changed link for",counter, "product")
# counter = 0

mytree.write('output.xml')
mytree.write('feed.xml')
