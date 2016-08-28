# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator
from page.models import ItemInfo
from mongoengine import *
connect('ganji', host='127.0.0.1', port=27017)
# Create your views here.


def pure_index(request):
    limit = 10
    item_info = ItemInfo.objects
    paginator = Paginator(item_info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)
    context = {
        'ItemInfo': loaded,
        'counts': item_info.count()
    }
    return render(request, 'index.html', context)


def home(request):
    limit = 10
    item_info = ItemInfo.objects
    paginator = Paginator(item_info, limit)
    print(paginator.num_pages)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)
    context = {
        'ItemInfo': loaded,
        'counts': item_info.count()
    }
    return render(request, 'pure_index_paginator.html', context)




def top3(date1, date2, area, limit):
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': date1, '$lte': date2}}, {'area': {'$all': area}}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts':{'$sum': 1}}},
        {'$limit': limit},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data

series_CY = [i for i in top3('2015.12.25', '2015.12.27', ['朝阳'], 3)]
series_HD = [i for i in top3('2015.12.25', '2015.12.27', ['海淀'], 3)]
series_TZ = [i for i in top3('2015.12.25', '2015.12.27', ['通州'], 3)]


def total_post():
    pipeline = [
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data
series_post = [i for i in total_post()]


def one_day_deal_area():
    pipeline = [
            {'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.01.11'}}, {'time': 1}]}},
            {'$group': {'_id': {'$slice': ['$area', 1]}, 'counts': {'$sum': 1}}},
            {'$sort': {'counts': 1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data

pie_data_area = [i for i in one_day_deal_area()]


def one_day_deal_cate():

    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.01.11'}}, {'time': 1}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data

pie_data_cate = [i for i in one_day_deal_cate()]


def chart(request):
    context = {
        'chart_CY': series_CY,
        'chart_TZ': series_TZ,
        'chart_HD': series_HD,
        'series_post': series_post,
        'pie1_data': pie_data_cate,
        'pie2_data': pie_data_area
    }
    return render(request, 'chart.html', context)
