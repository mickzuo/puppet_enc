from  yaml import dump,load
import types

document = """
name: Vorlin Laruknuzum
sex: Male
class: Priest
title: Acolyte
hp: [32, 71]
sp: [1, 13]
gold: 423
inventory:
- a Holy Book of Prayers (Words of Wisdom)
- an Azure Potion of Cure Light Wounds
- a Silver Wand of Wonder
"""
a=load(document)
print(a)
#print(dump(load(document)))
#print(dump(load(document)),default_flow_style=False)
#打印由字符转换成python对象的yaml格式信息
#stream = file('document.yaml', 'w')
#dump(yaml.load(document), stream)
#写文件    # Write a YAML representation of data to 'document.yaml'.
#print dump(yaml.load(document)) 
