#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from store.service import Service

def main():
    service = Service()
    service.drop_tables()
    service.create_tables()

if __name__ == '__main__':
    main()
