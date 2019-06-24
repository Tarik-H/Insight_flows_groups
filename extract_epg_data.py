import requests, json, copy
import xlsxwriter

headers = { 'Content-Type': "application/json" }
es_url = 'http://172.28.46.226:9200/elastiflow-*/_search'

dns_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "dns (UDP/53)"}},
        {"term": {"flow.service_name": "dns (TCP/53)"}},
        {"term": {"flow.application": "DNS"}},
        {"term": {"flow.application": "DNScrypt"}},
        {"term": {"flow.application": "MDNS"}},
        {"term": {"flow.application": "OpenDNS"}}
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}


dns_local={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "dns (UDP/53)"}},
        {"term": {"flow.service_name": "dns (TCP/53)"}},
        {"term": {"flow.application": "DNS"}},
        {"term": {"flow.application": "DNScrypt"}},
        {"term": {"flow.application": "MDNS"}},
        {"term": {"flow.application": "OpenDNS"}}
      ],
      "minimum_should_match" : 1,
      "must": {
        "term": {"flow.traffic_locality": "private"}
      }
    }
  },  
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service_name": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}


ad_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "ldap (TCP/389)"}},
        {"term": {"flow.service_name": "ldap (UDP/389)"}},
        {"term": {"flow.service_name": "netbios-ssn (TCP/139)"}},
        {"term": {"flow.service_name": "adws (TCP/9389)"}},
        {"term": {"flow.service_name": "msft-gc-ssl (TCP/3269)"}},
        {"term": {"flow.service_name": "msft-gc (TCP/3268)"}},
        {"term": {"flow.service_name": "ldaps (TCP/636)"}},
        {"term": {"flow.service_name": "microsoft-ds (TCP/445)"}},
        {"term": {"flow.service_name": "epmap (TCP/135)"}},
        {"term": {"flow.service_name": "kerberos (TCP/88)"}},
        {"term": {"flow.service_name": "kerberos UDP/88)"}}  
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

dhcp_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "bootps (UDP/67)"}},
        {"term": {"flow.service_name": "bootps (TCP/67)"}},
        {"term": {"flow.service_name": "bootpc (UDP/68)"}},
        {"term": {"flow.service_name": "bootpc (TCP/68)"}}        
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

smtp_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "smtp (UDP/25)"}},
        {"term": {"flow.service_name": "smtp (TCP/25)"}},
        {"term": {"flow.application": "SMTP"}}
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

ntp_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "ntp (UDP/123)"}},
        {"term": {"flow.service_name": "ntp (TCP/123)"}}    
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

ftp_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "ftp (TCP/21)"}},
        {"term": {"flow.service_name": "ftp-data (TCP/20)"}},
        {"term": {"flow.service_name": "ftps-data (TCP/989)"}}
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

sql_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.service_name": "mysqlx (TCP/33060)"}},
        {"term": {"flow.service_name": "sql-net (TCP/66)"}},
        {"term": {"flow.service_name": "sqlserv (TCP/118)"}},
        {"term": {"flow.service_name": "sql-net (TCP/150)"}},
        {"term": {"flow.service_name": "sqlsrv (TCP/156)"}},
        {"term": {"flow.service_name": "mini-sql (TCP/1114)"}},
        {"term": {"flow.service_name": "mysql-cluster (TCP/1186)"}},
        {"term": {"flow.service_name": "ms-sql-s (TCP/1433)"}},
        {"term": {"flow.service_name": "ms-sql-m (TCP/1434)"}},
        {"term": {"flow.service_name": "sybase-sqlany (TCP/1498)"}},
        {"term": {"flow.service_name": "oracle-sqlnet (TCP/1521)"}},
        {"term": {"flow.service_name": "mysql-cm-agent (TCP/1862)"}},
        {"term": {"flow.service_name": "unisql (TCP/1978)"}},
        {"term": {"flow.service_name": "unisql-java (TCP/1979)"}},
        {"term": {"flow.service_name": "mysql-im (TCP/2273)"}},
        {"term": {"flow.service_name": "mysql (TCP/3306)"}},
        {"term": {"flow.service_name": "ssql (TCP/3352)"}},
        {"term": {"flow.service_name": "rsqlserver (TCP/4430)"}},
        {"term": {"flow.service_name": "postgresql (TCP/5432)"}},
        {"term": {"flow.service_name": "postgresql9 (TCP/5433)"}},
        {"term": {"flow.service_name": "oracle-sqlplus-http (TCP/5560)"}},
        {"term": {"flow.service_name": "oracle-sqlplus-jms (TCP/5600)"}},
        {"term": {"flow.service_name": "mysql-proxy (TCP/6446)"}},
        {"term": {"flow.service_name": "sqlexec (TCP/9088)"}},
        {"term": {"flow.service_name": "sqlexec-ssl (TCP/9089)"}},
        {"term": {"flow.service_name": "gds-db (TCP/3050)"}},
        {"term": {"flow.service_name": "ttc (TCP/2483)"}},
        {"term": {"flow.service_name": "ttc-ssl (TCP/2484)"}},
        {"term": {"flow.service_name": "giop (TCP/2481)"}},
        {"term": {"flow.service_name": "giop-ssl (TCP/2482)"}},
        {"term": {"flow.service_name": "rdb-dbs-disp (TCP/1571)"}},
        {"term": {"flow.service_name": "oraclenames (TCP/1575)"}},
        {"term": {"flow.service_name": "oracle-em1 (TCP/1748)"}},
        {"term": {"flow.service_name": "oracle-emdb-rmi (TCP/5520)"}},
        {"term": {"flow.service_name": "oracle-emdb-jms (TCP/5540)"}},
        {"term": {"flow.service_name": "oracle-sqlplus-http (TCP/5560)"}},
        {"term": {"flow.service_name": "oracleas-https (TCP/7443)"}},
        {"term": {"flow.application": "Oracle"}},
        {"term": {"flow.application": "MsSQL-TDS"}},
        {"term": {"flow.application": "PostgreSQL"}},
        {"term": {"flow.application": "MySQL"}},
        {"term": {"flow.service_name": "mongodb (TCP/27017)"}},
        {"term": {"flow.service_name": "nbdb (TCP/13785)"}},
        {"term": {"flow.service_name": "mimer (TCP/1360)"}},
        {"term": {"flow.service_name": "bolt (TCP/7687)"}},
        {"term": {"flow.service_name": "ctdp (TCP/7022)"}},
        {"term": {"flow.service_name": "couchdb (TCP/5984)"}},
        {"term": {"flow.service_name": "sybaseanywhere (TCP/2638)"}},
        {"term": {"flow.service_name": "tlisrv (TCP/1527)"}},
        {"term": {"flow.service_name": "powerexchange (TCP/2480)"}},
        {"term": {"flow.service_name": "ctdp (TCP/7022)"}},
        {"term": {"flow.service_name": "ctdp (TCP/7022)"}}
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}

vmware_raw={ 
  "query": {
    "bool":{
      "should": [
        {"term": {"flow.application": "VMWARE"}},
        {"term": {"flow.service_name": "ideafarm-door (TCP/902)"}}
      ]
    }  
  },   
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 1000,
        "sources": [
          {"Producer": {"terms": {"field": "flow.server_addr"}}},
          {"Consumer": {"terms": {"field": "flow.client_addr"}}},          
          {"service": {"terms": {"field": "flow.service_name"}}}                  
        ]
      }
    }
  }
}


######### ES API calls 

def getting_data(service_type,ctx,contract,subj,filt,pro_epg):
    raw_data = json.dumps(service_type)
    resp = requests.request("GET", url=es_url, data=raw_data, headers=headers)
    re = json.loads(resp.text)
    #print(resp.content)
    #print(dir(resp))
    obj = re['aggregations']['table']['buckets']
    for entry in obj:
    	entry['key'].update({'context': ctx, 'contract_name': contract, 'subject_name': subj, 'filter_name': filt, 'prov_epg': pro_epg})
    return obj

dns_data = getting_data(dns_raw,'common_services', 'shared_infra', 'DNS_subject', 'DNS_filter', 'AD_epg')

ad_data = getting_data(ad_raw, 'common_services', 'Windows_controllers', 'AD_subject', 'AD_filter', 'AD_epg')

dhcp_data = getting_data(dhcp_raw, 'common_services', 'shared_infra', 'DHCP_subject', 'DHCP_filter', 'DHCP_epg')

smtp_data = getting_data(smtp_raw, 'common_services', 'shared_infra', 'SMTP_subject', 'SMTP_filter', 'SMTP_epg')

ntp_data = getting_data(ntp_raw, 'common_services', 'shared_infra', 'NTP_subject', 'NTP_filter', 'NTP_epg')

ftp_data = getting_data(ftp_raw, 'common_services', 'file_shares', 'FTP_subject', 'FTP_filter', 'FTP_epg')

sql_data = getting_data(sql_raw, 'shared_databases', 'shared_databases', 'SQL_subject', 'SQL_filter', 'DB_epg')

vmware_data = getting_data(vmware_raw, 'common_services', 'shared_orchestrators', 'VMWARE_subject', 'VMWARE_filter', 'VSPHERE_epg')

#monitoring_data = getting_data(monitoring_raw, 'common_services', 'shared_orchestrators', 'VMWARE_subject', 'VMWARE_filter', 'VSPHERE_epg')

service_data = [dns_data, ad_data, dhcp_data, smtp_data, ntp_data, ftp_data, sql_data, vmware_data]
# print(ftp_data)
# for ou in service_data:
# 	for out in ou:
# 		#print( out)
# 		for k,v in out.items():
# 			#print(type(v))
# 			print(k,v)


######## Helper functions

excel_file = "./" + "common_services.xlsx" ##file location


def getValue(d = {}, k = ''):
    ''' Function to retrieve a value for the key 'k' from the dict 'd'. Return "n/a" if the key does not exists '''
    if k in d:
        return d[k]
    else:
        return 'n/a'

def toggle_value(input):
    '''
    Function to toggle boolean input, and integer input of 1 and 0
    '''
    output = input
    return not output

######## Creating the output Excel file

def create_excel(excel_file):
    '''
    Function to create an excel file containing tenant information
    '''
    wb = xlsxwriter.Workbook(excel_file)
    ws1 = wb.add_worksheet('Suggested_services')
    format1 = wb.add_format({'bg_color': '#FFFFFF', 'border': 7})
    format2 = wb.add_format({'bg_color': '#F0F0F0', 'border': 7})
    cell_formats = [format1, format2]
    row = 0
    col = 0
    format_sel = 0
    loop_format = cell_formats[format_sel]

    headline1 = ['scope','contract_name','subject_name','filter_name', 'service', 'consumer_endpoint','provider_endpoint', 'provider_EPG']

    # write headline4
    row = 0
    col = 0
    line_index = ''
    line_index_old = ''
    format_sel = 0
    loop_format = cell_formats[format_sel]
    for hl in headline1:
        ws1.write(row, col, hl)
        col += 1
    # pprint(l3outs)

    for uo in service_data:
        for out in uo:
            line_index = '' + getValue(out['key'], 'Producer') + getValue(out['key'], 'Consumer') + getValue(out['key'], 'service_name')
            if line_index != line_index_old:
               format_sel = toggle_value(format_sel)
               loop_format = cell_formats[format_sel]
               line_index_old = line_index
            row += 1
            col = 0
            ws1.write(row, col, getValue(out['key'], 'context'), loop_format)
            col += 1
            ws1.write(row, col, getValue(out['key'], 'contract_name'), loop_format)
            col += 1
            ws1.write(row, col, getValue(out['key'], 'subject_name'), loop_format)
            col += 1
            ws1.write(row, col, getValue(out['key'], 'filter_name'), loop_format)
            col += 1
            ws1.write(row, col, getValue(out['key'], 'service'), loop_format)
            col += 1            
            ws1.write(row, col, getValue(out['key'], 'Consumer'), loop_format)
            col += 1            
            ws1.write(row, col, getValue(out['key'], 'Producer'), loop_format)
            col += 1
            ws1.write(row, col, getValue(out['key'], 'prov_epg'), loop_format)
            col += 1            
    # set column width to 25 and apply auto-filter
    ws1.set_column(0, col, 18)
    ws1.autofilter(0, 0, row, col-1)
    ws1.freeze_panes(1, 1)

    wb.close()   ####  Close the entire Workbook

print("#########################################################################################################################")
print("#########################################################################################################################")

print("Create Excel\n")
create_excel(excel_file)

print("#########################################################################################################################")
print("#########################################################################################################################")