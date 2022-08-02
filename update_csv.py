from csv import DictWriter


def updater(data={}):
    with open(f'data.csv', 'a',newline='') as f_object:
        field_names = ['name','url','email','phno','service']
        writer_object = DictWriter(f_object,fieldnames=field_names)
        writer_object.writerow(data)
        f_object.close()

if __name__ == "__main__":
    updater(data={'name':'','url':'','email':'','phno':'','service':''})
