
 
import sys   
version = (3, 0)
cur_version = sys.version_info
if cur_version >= version:   
     
    import urllib.request
    from urllib.request import Request, urlopen
    from urllib.request import URLError, HTTPError
    from urllib.parse import quote
else:   
     
    import urllib2
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urllib import quote
import time   
import os
import argparse
import ssl
import datetime

 
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keywords', help='delimited list input', type=str, required=False)
parser.add_argument('-u', '--url', help='search with google image URL', type=str, required=False)
parser.add_argument('-l', '--limit', help='delimited list input', type=str, required=False)
parser.add_argument('-x', '--single_image', help='downloading a single image from URL', type=str, required=False)
parser.add_argument('-o', '--output_directory', help='download images in a specific directory', type=str, required=False)
parser.add_argument('-d', '--delay', help='delay in seconds to wait between downloading two images', type=str, required=False)
parser.add_argument('-c', '--color', help='filter on color', type=str, required=False,
                    choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
parser.add_argument('-r', '--usage_rights', help='usage rights', type=str, required=False,
                    choices=['labled-for-reuse-with-modifications','labled-for-reuse','labled-for-noncommercial-reuse-with-modification','labled-for-nocommercial-reuse'])
parser.add_argument('-s', '--size', help='image size', type=str, required=False,
                    choices=['large','medium','icon'])
parser.add_argument('-t', '--type', help='image type', type=str, required=False,
                    choices=['face','photo','clip-art','line-drawing','animated'])
parser.add_argument('-w', '--time', help='image age', type=str, required=False,
                    choices=['past-24-hours','past-7-days'])

args = parser.parse_args()

if args.keywords:
    search_keyword = [str(item) for item in args.keywords.split(',')]
 
if args.limit:
    limit = int(args.limit)
    if int(args.limit) >= 100:
        limit = 100
else:
    limit = 100

 
if args.single_image is None and args.url is None and args.keywords is None:
            parser.error('Keywords is a required argument!')

if args.output_directory:
    main_directory = args.output_directory
else:
    main_directory = "downloads"

if args.delay:
    try:
        val = int(args.delay)
    except ValueError:
        parser.error('Delay parameter should be an integer!')

main_directory = main_directory + "/train"

 
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:   
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:   
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(req)
            except URLError:   
                context = ssl._create_unverified_context()
                response = urlopen(req, context=context)
            page = response.read()
            return page
        except:
            return "Page Not found"


 
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:   
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


 
def _images_get_all_items(page):
    items = []
    a = 0
    while a < limit:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)   
            time.sleep(0.1)   
            page = page[end_content:]
        a += 1
    return items


 
def build_url_parameters():
    built_url = "&tbs="
    counter = 0
    params = {'color':[args.color,{'red':'ic:specific,isc:red', 'orange':'ic:specific,isc:orange', 'yellow':'ic:specific,isc:yellow', 'green':'ic:specific,isc:green', 'teal':'ic:specific,isc:teel', 'blue':'ic:specific,isc:blue', 'purple':'ic:specific,isc:purple', 'pink':'ic:specific,isc:pink', 'white':'ic:specific,isc:white', 'gray':'ic:specific,isc:gray', 'black':'ic:specific,isc:black', 'brown':'ic:specific,isc:brown'}],
              'usage_rights':[args.usage_rights,{'labled-for-reuse-with-modifications':'sur:fmc','labled-for-reuse':'sur:fc','labled-for-noncommercial-reuse-with-modification':'sur:fm','labled-for-nocommercial-reuse':'sur:f'}],
              'size':[args.size,{'large':'isz:l','medium':'isz:m','icon':'isz:i'}],
              'type':[args.type,{'face':'itp:face','photo':'itp:photo','clip-art':'itp:clip-art','line-drawing':'itp:lineart','animated':'itp:animated'}],
              'time':[args.time,{'past-24-hours':'qdr:d','past-7-days':'qdr:w'}]}
    for key, value in params.items():
        if value[0] is not None:
            ext_param = value[1][value[0]]
             
             
            if counter == 0:
                 
                built_url = built_url + ext_param
                counter += 1
            else:
                built_url = built_url + ',' + ext_param
                counter += 1
    return built_url

 
t0 = time.time()   
 
if args.single_image:
    url = args.single_image
    try:
        os.makedirs(main_directory)
    except OSError as e:
        if e.errno != 17:
            raise
             
        pass
    req = Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
    response = urlopen(req, None, 15)
    image_name = str(url[(url.rfind('/')) + 1:])
    if '?' in image_name:
        image_name = image_name[:image_name.find('?')]
    if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
        output_file = open(main_directory + "/" + image_name, 'wb')
    else:
        output_file = open(main_directory + "/" + image_name + ".jpg", 'wb')
        output_file = open(main_directory + "/" + image_name + ".jpg", 'wb')
        image_name = image_name + ".jpg"

    data = response.read()
    output_file.write(data)
    response.close()

    print("completed ====> " + image_name)
 
else:
     
    errorCount = 0
    i = 0
    if args.url:
        search_keyword = [str(datetime.datetime.now()).split('.')[0]]
     
    while i < len(search_keyword):
        items = []
        iteration = "\n" + "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(search_keyword[i])
        print(iteration)
        print("Evaluating...")
        search_term = search_keyword[i]
        dir_name = search_term + ('-' + args.color if args.color else '')

         
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
                path = str(dir_name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = str(dir_name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
        except OSError as e:
            if e.errno != 17:
                raise
                 
            pass

        j = 0

        params = build_url_parameters()
         
         
        if args.url:
            url = args.url
        else:
            url = 'https://www.google.com/search?q=' + quote(search_term) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html = (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        print("Total Image Links = " + str(len(items)))

         
        info = open('logs', 'a')   
        info.write(str(i) + ': ' + str(search_keyword[i - 1]) + ": " + str(items))   
        info.close()   

        t1 = time.time()   
        total_time = t1 - t0   
        print("Total time taken: " + str(total_time) + " Seconds")
        print("Starting Download...")

         
         
        k = 0
        par = round(limit*.2)  
        kk = 0 
        flag = 0
        while (k < limit):
            try:
                req = Request(items[k], headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
                response = urlopen(req, None, 15)
                image_name = str(items[k][(items[k].rfind('/')) + 1:])
                image_name = search_term + "_" + str(k)
                if k+1 >= (limit-par):
                    if flag == 0:
                        dir_name = "../test/" + dir_name
                        flag = 1
                        try:
                            if not os.path.exists(main_directory):
                                os.makedirs(main_directory)
                                time.sleep(0.2)
                                path = str(dir_name)
                                sub_directory = os.path.join(main_directory, path)
                                if not os.path.exists(sub_directory):
                                    os.makedirs(sub_directory)
                                    os.makedirs("datasets/trainX")
                                    os.makedirs("datasets/testX")
                            else:
                                path = str(dir_name)
                                sub_directory = os.path.join(main_directory, path)
                                if not os.path.exists(sub_directory):
                                    os.makedirs(sub_directory)
                                    os.makedirs("datasets/trainX")
                                    os.makedirs("datasets/testX")
                        except OSError as e:
                                if e.errno != 17:
                                    raise
                                pass

                    image_name = str(kk);
                    print("HHH " + str(image_name)+ " "+ str(dir_name))
                    kk = kk + 1
 
 
                if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
                    output_file = open(main_directory + "/" + dir_name + "/" + image_name, 'wb')
                else:
                    output_file = open(main_directory + "/" + dir_name + "/" + image_name + ".jpg", 'wb')
 

                data = response.read()
                output_file.write(data)
                response.close()

                print("completed ====> " + str(k + 1) + ". " + image_name)

                k = k + 1

            except IOError:   
                errorCount += 1
                print("IOError on " + str(k + 1))
                k = k + 1

            except HTTPError as e:   
                errorCount += 1
                print("HTTPError" + str(k))
                k = k + 1

            except URLError as e:
                errorCount += 1
                print("URLError " + str(k))
                k = k + 1

            except ssl.CertificateError as e:
                errorCount += 1
                print("CertificateError " + str(k))
                k = k + 1

            if args.delay:
                time.sleep(int(args.delay))

        i = i + 1

    print("\n")
    print("Download completato con successo")
    print("Totale Errori: " + str(errorCount) + "\n")
