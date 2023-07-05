from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator


def depart_list(request):
    depart_info = models.department.objects.all()

    return render(request, "depart/depart_list.html", {"depart_info": depart_info})


def depart_add(request):
    """添加部门"""
    # return render(request, "depart_add.html")
    # 进行判断，如果为GET请求，直接进入添加页面；否则执行添加操作
    if request.method == "GET":
        return render(request, "depart/depart_add.html")
    title = request.POST.get("title")
    models.department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""

    # 获取ID
    nid = request.GET.get("nid")

    # 删除
    models.department.objects.filter(id=nid).delete()

    # 重定向到列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """修改部门"""
    if request.method == "GET":
        row_object = models.department.objects.filter(id=nid).first()
        return render(request, "depart/depart_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    models.department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def user_list(request):
    users = models.user.objects.all()
    departments = models.department.objects.all()

    return render(request, "user/user_list.html", {"user_list": users, "department_list": departments})


class myForm(forms.ModelForm):
    class Meta:
        model = models.user_info
        fields = ["name", "passwd", "age", "account", "create_time", "depart", "gender"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    if request.method == "GET":
        form = myForm()
        return render(request, "user/user_add.html", {"form": form})

    form = myForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user/user_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.user_info.objects.filter(id=nid).first()
    if request.method == "GET":
        form = myForm(instance=row_object)
        return render(request, "user/user_edit.html", {"form": form})
    form = myForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user/user_edit.html", {"form": form})


def user_delete(request):
    nid = request.GET.get("nid")

    # 删除
    models.user_info.objects.filter(id=nid).delete()

    # 重定向到列表
    return redirect("/user/list/")


from app01.utiles.pageination import Pageination


def phone_list(request):
    # for i in range(300):
    #     models.phone_num_info.objects.create(phone="16619880393", price=99, status=1, level=2)
    date_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        date_dict["phone__contains"] = search_data

    phone = models.phone_num_info.objects.filter(**date_dict).order_by("status")

    page_object = Pageination(request, phone)
    page_queryset = page_object.page_queryset

    page_string = page_object.html()

    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }

    return render(request, "phone_num/phone_list.html", context)


class phoneAdd(forms.ModelForm):
    """ 靓号类添加 """
    # 手机号输入值校验
    phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.phone_num_info
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_phone(self):
        txt_phone = self.cleaned_data["phone"]
        exists = models.phone_num_info.objects.filter(phone=txt_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_phone


def phone_add(request):
    """ 添加靓号"""
    if request.method == "GET":
        form = phoneAdd()
        return render(request, "phone_num/phone_add.html", {"form": form})

    form = phoneAdd(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/phone/list/")
    return render(request, "phone_num/phone_add.html", {"form": form})


class phoneEdit(forms.ModelForm):
    """ 靓号类编辑 """
    # 手机号输入值校验
    phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.phone_num_info
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_phone(self):

        txt_phone = self.cleaned_data["phone"]
        exists = models.phone_num_info.objects.exclude(id=self.instance.id).filter(phone=txt_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_phone


def phone_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.phone_num_info.objects.filter(id=nid).first()
    if request.method == "GET":
        form = phoneEdit(instance=row_object)
        return render(request, "phone_num/phone_edit.html", {"form": form})

    form = phoneEdit(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return redirect("/phone/list/")
    return render(request, "phone_num/phone_edit.html", {"form": form})


def phone_delete(request):
    """ 删除靓号 """
    nid = request.GET.get("nid")

    # 删除
    models.phone_num_info.objects.filter(id=nid).delete()

    # 重定向到列表
    return redirect("/phone/list/")


######################### things_operator##########################
def things_type_list(request):
    things_type_list = models.things_type.objects.all()

    return render(request, "things_type/things_type_list.html", {"things_type_list": things_type_list})


class thingsAdd(forms.ModelForm):
    """ 添加类别类 """

    class Meta:
        model = models.things_type
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环添加样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_event(self):

        txt_things_type2 = self.cleaned_data["things_type2"]
        exists = models.event_list.objects.filter(things_type2=txt_things_type2).exists()
        if exists:
            raise ValidationError("类别已存在")
        return txt_things_type2


def things_type_add(request):
    """ 添加类别 """
    if request.method == "GET":
        form = thingsAdd()
        return render(request, "things_type/things_type_add.html", {"form": form})
    form = thingsAdd(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/things/list/")
    return redirect(request, "things_type/things_type_add.html", {"form": form})


class thingsEdit(forms.ModelForm):
    """ 类编辑 """

    class Meta:
        model = models.things_type
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_things_type(self):

        txt_things_type = self.cleaned_data["things_type"]
        exists = models.things_type.objects.exclude(id=self.instance.id).filter(things_type=txt_things_type).exists()
        if exists:
            raise ValidationError("类别已存在")
        return txt_things_type


def things_type_edit(request, nid):
    """ 编辑类别 """
    row_object = models.things_type.objects.filter(id=nid).first()
    if request.method == "GET":
        form = thingsEdit(instance=row_object)
        return render(request, "things_type/things_type_edit.html", {"form": form})

    form = thingsEdit(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return redirect("/things/list/")
    return render(request, "things_type/things_type_edit.html", {"form": form})


def things_type_delete(request):
    """删除类别"""
    # 获取ID
    nid = request.GET.get("nid")

    # 删除
    models.things_type.objects.filter(id=nid).delete()

    # 重定向到列表
    return redirect("/things/list/")


############################### 工单内容 ###############################


def event_list(request):
    event_list = models.event_list.objects.all()
    return render(request, "event/event_list.html", {"event_list": event_list})


class EventAdd(forms.ModelForm):
    """ 添加工单类 """

    class Meta:
        model = models.event_list
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环添加样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_event(self):
        txt_event = self.cleaned_data["event_number"]
        exists = models.event_list.objects.filter(event_number=txt_event).exists()
        if exists:
            raise ValidationError("工单号已存在")
        return txt_event


def event_add(request):
    """ 添加工单"""
    if request.method == "GET":
        form = EventAdd()
        return render(request, "event/event_add.html", {"form": form})

    form = EventAdd(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/event/list/")
    return redirect(request, "event_add.html", {"form": form})


def event_edit(request, nid):
    """ 编辑工单 """
    row_object = models.event_list.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID从数据库获取要编辑的数据
        form = EventAdd(instance=row_object)
        return render(request, "event/event_edit.html", {"form": form})

    form = EventAdd(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/event/list/")
    return redirect(request, "event/event_edit.html", {"form": form})


def event_delete(request):
    nid = request.GET.get("nid")

    # 删除
    models.event_list.objects.filter(id=nid).delete()

    # 重定向到列表
    return redirect("/event/list/")


# 案例：用户管理
def info_list(request):
    form = models.info_user.objects.all()
    return render(request, "info_list.html", {"form": form})


from app01.models import info_user


def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html")

    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    mail = request.POST.get("mail")

    info_user.objects.create(name=name, passwd=pwd, age=age, mail=mail)

    return redirect("/info/list/")


def info_delete(request):
    nid = request.GET.get("nid")
    info_user.objects.filter(id=nid).delete()
    return redirect("/info/list/")
