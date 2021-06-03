import csv
import urllib.request
import urllib.error
# from bs4 import BeautifulSoup
# import pandas as pd
import time

csv_path = '../small_subsets/Movies_and_TV/'
csv_filename = 'meta_Movies_and_TV.csv'
csv_out_filename = 'meta_Movies_and_TV_valid.csv'

start = time.time()
print('start', start)
# row_names = ['movie_id', 'movie_url']
# with open('movie_url3.csv', 'r', newline='') as in_csv:
with open(csv_path+csv_filename, 'r', newline='') as in_csv:
    # reader = csv.DictReader(in_csv, fieldnames=row_names, delimiter=',')
    reader = csv.DictReader(in_csv, delimiter=',')
    # sess to add the header for the output csv  !!!
    # with open(csv_path + csv_out_filename, 'a', newline='') as out_csv:
    #     writer = csv.writer(out_csv, delimiter=',')
    #     headers = reader.fieldnames
    #     headers.append('path')
    #     writer.writerow(headers)
    no_img_item_id = []
    no_img_item_url = []
    flag = True
    for row in reader:
        item_id = row['asin']
        image_url = row['imUrl']
        # sess for test the failure sample !!!
        if flag & (item_id != 'B0053IBTJK'):
            continue
        flag = False
        if 'no-img-sm' in image_url:
            print(image_url + ' is not valid')
            no_img_item_id.append(item_id)
            no_img_item_url.append(image_url)
            continue
        extension = image_url[-4:]
        filename = csv_path+'img/' + item_id + extension
        try:
            with urllib.request.urlopen(image_url, timeout=90) as response:
                with open(filename, 'wb') as out_image:
                    out_image.write(response.read())
                with open(csv_path+csv_out_filename, 'a', newline='') as out_csv:
                    writer = csv.writer(out_csv, delimiter=',')
                    row['path'] = filename
                    row_list = list(row.values())
                    writer.writerow(row_list)
        # Ignore cases where no poster image is present
        except (ValueError, urllib.error.HTTPError, urllib.error.URLError):
            print(item_id + ' image can not be accessed or time out after 3, imUrl is' + image_url)
            no_img_item_id.append(item_id)
            no_img_item_url.append(image_url)
            pass

        print('item_id:', item_id)
with open('no_image_item.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(no_img_item_id)
    wr.writerow(no_img_item_url)
print('time:', time.time()-start)

