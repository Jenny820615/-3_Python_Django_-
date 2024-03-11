from django.shortcuts import render, redirect
from myapp import models
from django.http import HttpResponse
# from django.http import JsonResponse
from myapp.models import Product
import math
from django.contrib.auth import authenticate
from django.contrib import auth
# from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText

def index(request):
    products = Product.objects.all()  # 從資料庫載入資料
    product_list = Product.objects.filter(product_sale=1)
    return render(request, 'index.html', {'products': products,'product_list': product_list})

def product(request):
    products = Product.objects.all()  # 從資料庫載入資料
    return render(request, 'product.html', {'products': products})

def adduser(request):
    try:
        # user=User.objects.get(username="test")
        user=User.objects.get(username="jenny")
    except:
        user=None
    if user!=None:
        message=user.username+"帳號已建立!"
        return HttpResponse(message)
    else: # 建立test帳號
        user=User.objects.create_user("admin2","admin2@gmail.com","admin123456")
        user.first_name="王" #姓名
        user.lase_name="小明" # 姓氏
        user.is_staff=True # 工作人員狀態
        user.save()
        return redirect("/admin/")

def login(request):  # 登入
    messages = ''  # 初始時清除訊息
    if request.method == 'POST':  # 如果是以POST方式才處理
        name = request.POST['username'].strip()  # 取得輸入帳號
        password = request.POST['password']  # 取得輸入密碼
        user1 = authenticate(username=name, password=password)  # 驗證
        if user1 is not None:  # 驗證通過
            if user1.is_active:  # 帳號有效
                auth.login(request, user1)  # 登入
                return redirect('/adminmain/')  # 開啟管理頁面
            else:  # 帳號無效
                messages = '帳號尚未啟用！'
        else:  # 驗證未通過
            messages = '登入失敗！'
    return render(request, "login.html", locals())

def logout(request):  # 登出
	auth.logout(request)
	return redirect('/')

def adminmain(request, pageindex=None):  # 管理頁面    
    global page1
    pagesize = 5
    products = Product.objects.all().order_by('-product_id')
    datasize = len(products)
    totpage = math.ceil(datasize / pagesize)
    if pageindex==None:
        page1 = 1
        products = Product.objects.all().order_by('-product_id')[:pagesize]
    elif pageindex=='1':
        start = (page1-2)*pagesize
        if start >= 0:
            products = Product.objects.all().order_by('-product_id')[start:(start+pagesize)]
            page1 -= 1
    elif pageindex=='2':
        start = page1*pagesize
        if start < datasize:
            products = Product.objects.all().order_by('-product_id')[start:(start+pagesize)]
            page1 += 1
    elif pageindex=='3':
        start = (page1-1)*pagesize
        products = Product.objects.all().order_by('-product_id')[start:(start+pagesize)]
    currentpage = page1
    return render(request, "adminmain.html", locals())

def product_add(request):
    message = ''
    product_name = request.POST.get('product_name', '')
    product_price = request.POST.get('product_price', '')
    product_description = request.POST.get('product_description', '')
    product_sale = request.POST.get('product_sale', '')
    product_storage = request.POST.get('product_storage', '')
    try:
        product_sale = int(product_sale)
        if product_sale not in [1, 2]:
            product_sale = 0
    except ValueError:
        product_sale = 0
    try:
        product_storage = int(product_storage)
    except ValueError:
        product_storage = 0
    product_image_link = request.POST.get('product_image_link', '')

    ok = request.POST.get('product_ok', '')

    if product_name == '' or product_price == '' or product_image_link == '':
        message = '每一個欄位都要填寫...'
    else:
        if ok == 'yes':
            enabled = True
        else:
            enabled = False
        product = Product.objects.create(product_name=product_name, product_price=product_price, product_description=product_description,product_sale=product_sale, product_image_link=product_image_link,product_storage=product_storage)
        product.save()
        return redirect('/product_add/')
    return render(request, "product_add.html", locals())

def product_edit(request, product_id=None, edittype=None):  # 修改資料
    product = Product.objects.get(pk=product_id)   # 讀取指定資料
    if edittype == None:  # 進入修改頁面,顯示原有資料
        product_name = product.product_name
        product_price = product.product_price
        product_description = product.product_description
        product_sale = product.product_sale
        product_image_link = product.product_image_link
        product_storage = product.product_storage
    elif edittype == '1':  # 修改完畢,存檔
        product_name = request.POST.get('product_name', '')
        product_price = request.POST.get('product_price', '')
        product_description = request.POST.get('product_description', '')
        product_sale = request.POST.get('product_sale', '')
        product_storage = request.POST.get('product_storage', '')
        try:
            product_sale = int(product_sale)
            if product_sale not in [1, 2]:
                product_sale = 0
        except ValueError:
            product_sale = 0
        try:
            product_storage = int(product_storage)
        except ValueError:
            product_storage = 0
        product_image_link = request.POST.get('product_image_link', '')
        ok = request.POST.get('product_ok', '')
        if ok=='yes':
            enabled = True
        else:
            enabled = False
        product.product_name = product_name
        product.product_price = product_price
        product.product_description = product_description
        product.product_sale = product_sale
        product.product_image_link = product_image_link
        product.product_storage = product_storage
        product.enabled = enabled
        product.save()
        return redirect('/adminmain/')
    return render(request, "product_edit.html", locals())

def product_delete(request, product_id=None, deletetype=None):  # 刪除資料
    product = Product.objects.get(pk=product_id)   # 讀取指定資料
    if deletetype == None:  # 進入刪除頁面,顯示原有資料
        product_name = product.product_name
        product_price = product.product_price
        product_description = product.product_description
        product_sale = product.product_sale
        product_image_link = product.product_image_link
        product_storage = product.product_storage
    elif deletetype == '1':  # 按刪除鈕
        product.delete()
        return redirect('/adminmain/')
    return render(request, "product_delete.html", locals())

def albumindex(request):
    albums = models.AlbumModel.objects.all().order_by('-id')  # 讀取所有相簿
    totalalbum = len(albums)  # 相簿總數
    photos = []    # 每一相簿第1張相片串列
    lengths = []   # 每一相簿的相片總數串列
    for album in albums:
        photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  # 讀取相片
        lengths.append(len(photo))    # 加入相片總數
        if len(photo) == 0:           # 若無相片加入空字串
            photos.append('')
        else:
            photos.append(photo[0].purl)  #加入第1張相片
    return render(request, "albumindex.html", locals())
	
def albumshow(request, albumid=None):  # 顯示相簿
	album = albumid  # 以區域變數傳送給html
	photos = models.PhotoModel.objects.filter(palbum__id=album).order_by('-id')  #讀取所有相片
	monophoto = photos[0]      # 第1張相片
	totalphoto = len(photos)   # 相片總數
	return render(request, "albumshow.html", locals())
	
def albumphoto(request, photoid=None, albumid=None):       # 顯示單張相片
	album = albumid    # 以區域變數傳送給 html
	photo = models.PhotoModel.objects.get(id=photoid)      # 取得點選的相片
	photo.phit += 1    # 點擊數加1
	photo.save()       # 儲存資料
	return render(request, "albumphoto.html", locals())

def albumlogin(request):  # 登入
	messages = ''    # 初始時清除訊息
	if request.method == 'POST':  # 如果是以POST方式才處理
		name = request.POST['username'].strip()  # 取得輸入帳號
		password = request.POST['passwd']  # 取得輸入密碼
		user1 = authenticate(username=name, password=password)  # 驗證
		if user1 is not None:     # 驗證通過
			if user1.is_active:   # 帳號有效
				auth.login(request, user1)  # 登入
				return redirect('/albumadminmain/')  # 開啟管理頁面
			else:  # 帳號無效
				message = '帳號尚未啟用！'
		else:  # 驗證未通過
			message = '登入失敗！'
	return render(request, "albumlogin.html", locals())

def albumlogout(request):  # 登出
	auth.logout(request)
	return redirect('/albumindex/')

def albumadminmain(request, albumid=None):  # 管理頁面
	if albumid == None:  # 按相簿管理鈕進管理頁面
		albums = models.AlbumModel.objects.all().order_by('-id')
		totalalbum = len(albums)
		photos = []
		lengths = []
		for album in albums:
			photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
			lengths.append(len(photo))
			if len(photo) == 0:
				photos.append('')
			else:
				photos.append(photo[0].purl)
	else:  # 按刪除相簿鈕
		album = models.AlbumModel.objects.get(id=albumid)  # 取得相簿
		photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  # 取得所有相片
		for photounit in photo:  # 刪除所有相片檔案
			os.remove(os.path.join(settings.MEDIA_ROOT, photounit.purl ))
		album.delete()  # 移除相簿
		return redirect('/albumadminmain/')
	return render(request, "albumadminmain.html", locals())

def albumadminadd(request):  # 新增相簿
	message = ''
	title = request.POST.get('album_title', '')  # 取得輸入資料
	location = request.POST.get('album_location', '')
	desc = request.POST.get('album_desc', '')
	if title=='':  # 按新增相簿鈕進入此頁
		message = '相簿名稱必須填寫...'
	else:  #按確定新增鈕
		unit = models.AlbumModel.objects.create(atitle=title, alocation=location, adesc=desc)
		unit.save()
		return redirect('/albumadminmain/')
	return render(request, "albumadminadd.html", locals())

def albumadminfix(request, albumid=None, photoid=None, deletetype=None):  # 相簿維護
    album = models.AlbumModel.objects.get(id=albumid)  #取得指定相簿
    photos = models.PhotoModel.objects.filter(palbum__id=albumid).order_by('-id')
    totalphoto = len(photos)
    if photoid != None:         # 不是由管理頁面進入本頁面
        if photoid == 999999:   # 按更新及上傳資料鈕
            album.atitle = request.POST.get('album_title', '')  # 更新相簿資料
            album.alocation = request.POST.get('album_location', '')
            album.adesc = request.POST.get('album_desc', '')
            album.save()
            files = []  # 上傳相片串列
            descs = []  # 相片說明串列
            picurl = ["ap_picurl1", "ap_picurl2", "ap_picurl3", "ap_picurl4", "ap_picurl5"]
            subject = ["ap_subject1", "ap_subject2", "ap_subject3", "ap_subject4", "ap_subject5"]
            for count in range(0,5):
                files.append(request.FILES.get(picurl[count], ''))
                descs.append(request.POST.get(subject[count], ''))
            i = 0
            for upfile in files:  
                if upfile != '' and descs[i] != '':
                    fs = FileSystemStorage()  # 上傳檔案
                    filename = fs.save(upfile.name, upfile)
                    unit = models.PhotoModel.objects.create(palbum=album, psubject=descs[i], purl=upfile)  # 寫入資料庫
                    unit.save()
                    i += 1
            return redirect('/albumadminfix/' + str(album.id) + '/')
        elif deletetype == 'update':  # 更新相片說明
            photo = models.PhotoModel.objects.get(id=photoid)
            photo.psubject = request.POST.get('ap_subject', '')  # 取得相片說明
            photo.save()  # 寫入資料庫
            return redirect('/albumadminfix/' + str(album.id) + '/')
        elif deletetype=='delete':  # 刪除相片
            photo = models.PhotoModel.objects.get(id=photoid)
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.purl ))  # 刪除相片檔
            photo.delete()  # 從資料庫移除
            return redirect('/albumadminfix/' + str(album.id) + '/')
    return render(request, "albumadminfix.html", locals())

message = ''
cartlist = []        # 購買商品串列
customname = ''      # 購買者姓名
customphone = ''     # 購買者電話
customaddress = ''   # 購買者地址
customemail = ''     # 購買者電子郵件

# def cartindex(request):
# 	global cartlist
# 	if 'cartlist' in request.session:              # 若 session中存在cartlist就讀出
# 		cartlist = request.session['cartlist']
# 	else:                          # 重新購物
# 		cartlist = []
# 	cartnum = len(cartlist)        # 購買商品筆數
# 	productall = models.ProductModel.objects.all() # 取得資料庫所有商品
# 	return render(request, "cartindex.html", locals())

def detail(request, product_id=None):                         # 商品詳細頁面
	product = models.Product.objects.get(product_id=product_id)  # 取得商品
	return render(request, "detail.html", locals())

def cart(request):                 # 顯示購物車
	global cartlist
	cartlist1 = cartlist           # 以區域變數傳給模版
	total = 0
	for unit in cartlist:          # 計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100       # 加入運費總額
	return render(request, "cart.html", locals())

def addtocart(request, ctype=None, product_id=None):
	global cartlist
	if ctype == 'add':           # 加入購物車
  		product = models.Product.objects.get(product_id=product_id)
  		flag = True              # 設檢查旗標為True
  		for unit in cartlist:                    # 逐筆檢查商品是否已存在
  			if product.product_name == unit[0]:         # 商品已存在
  				unit[2] = str(int(unit[2])+ 1)   # 數量加1
  				unit[3] = str(int(unit[3]) + product.product_price)  # 計算價錢
  				flag = False     # 設檢查旗標為False
  				break
  		if flag:                 # 商品不存在
  			temlist = []         #  暫時串列
  			temlist.append(product.product_name)        # 將商品資料加入暫時串列
  			temlist.append(str(product.product_price))  # 商品價格
  			temlist.append('1')                  # 先暫訂數量為1
  			temlist.append(str(product.product_price))  # 總價
  			cartlist.append(temlist)             # 將暫時串列加入購物車
  		request.session['cartlist'] = cartlist   # 將購物車寫入session
  		return redirect('/cart/')
	elif ctype == 'update':      # 更新購物車
		n = 0
		for unit in cartlist:
			unit[2] = request.POST.get('qty' + str(n), '1')  # 取得數量
			unit[3] = str(int(unit[1]) * int(unit[2]))       # 取得總價
			n += 1
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
	elif ctype == 'empty':       # 清空購物車
		cartlist = []            # 設定購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/product/')
	elif ctype == 'remove':      # 刪除購物車中的商品
		del cartlist[int(product_id)]  # 從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/cart/')

def cartorder(request):          # 按我要結帳鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	cartlist1 = cartlist
	total = 0
	for unit in cartlist:        # 計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100
	customname1 = customname     # 以區域變數傳給模版
	customphone1 = customphone
	customaddress1 = customaddress
	customemail1 = customemail
	message1 = message
	return render(request, "cartorder.html", locals())

def cartok(request):             # 按確認購買鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	total = 0
	for unit in cartlist:
		total += int(unit[3])
	grandtotal = total + 100
	message = ''
	customname = request.POST.get('CustomerName', '')
	customphone = request.POST.get('CustomerPhone', '')
	customaddress = request.POST.get('CustomerAddress', '')
	customemail = request.POST.get('CustomerEmail', '')
	paytype = request.POST.get('paytype', '')
	customname1 = customname
	if customname=='' or customphone=='' or customaddress=='' or customemail=='':
		message = '姓名、電話、住址及電子郵件皆需輸入'
		return redirect('/cartorder/')
	else:
		unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype) # 建立訂單
		for unit in cartlist:         # 將購買的商品寫入資料庫
			total = int(unit[1]) * int(unit[2])
			unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
		orderid = unitorder.id        # 取得訂單id
		mailfrom="buzzz27516100@gmail.com"   # 帳號
		mailpw="sjpn pzew lxua mlpv"             # 應用程式密碼
		mailto=customemail            # 收件者
		mailsubject="Belle Baii-網路購物訂單通知";  # 郵件標題
		mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品寄送給您！ 再次感謝您的支持！\n您的訂單編號為：" + str(orderid) + "，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n~Belle Baii Scented Candles~" # 郵件內容
		send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent)  # 寄信
		cartlist = []
		request.session['cartlist'] = cartlist
		return render(request, "cartok.html", locals())

def cartordercheck(request):                    # 查詢訂單
	orderid = request.GET.get('orderid', '')    # 取得輸入的 id
	customemail = request.GET.get('customemail', '')  # 取得輸入的 email
	if orderid == '' and customemail == '':     # 按查詢訂單鈕
		firstsearch = 1
	else:
		order = models.OrdersModel.objects.filter(id=orderid).first()
		if order == None or order.customemail != customemail:  # 找不到資料
			notfound = 1
		else:  # 找到符合的資料
			details = models.DetailModel.objects.filter(dorder=order)
	return render(request, "cartordercheck.html", locals())

def send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent): # 寄信
	global message
	strSmtp = "smtp.gmail.com:587" #主機
	strAccount = mailfrom          # 帳號
	strPassword = mailpw           # 密碼
	msg = MIMEText(mailcontent)
	msg["Subject"] = mailsubject   # 郵件標題
	mailto1 = mailto               # 收件者
	server = SMTP(strSmtp)         # 建立 SMTP 連線
	server.ehlo()                  # 跟主機溝通
	server.starttls()              # TTLS 安全認證
	try:
		server.login(strAccount, strPassword)                 # 登入
		server.sendmail(strAccount, mailto1, msg.as_string()) # 寄信
	except SMTPAuthenticationError:
		message = "無法登入！"
	except:
		message = "郵件發送產生錯誤！"
	server.quit() # 關閉連線