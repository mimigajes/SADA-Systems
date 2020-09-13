import boto3, botocore
import os
import hashlib



s3= boto3.client('s3')


def handler(event,context):
    path = (event['Records'][0]['s3']['object']['key'])
    bucket = (event['Records'][0]['s3']['bucket']['name'])
    flname = path.split("/")[-1]
    filetype = flname.split('.')[-1]
    #print(f'You uploaded {flname} in {bucket} and the file type is {filetype}')
    #print(path)
    
    os.makedirs(os.path.dirname(f'/tmp/{flname}'), exist_ok=True)
    s3.download_file(bucket, path, f'/tmp/{flname}')
    all_line = 0
    real_line = 0
    Hashes = []
    dupes = []
    write_line = []
    
    with open(f'/tmp/{flname}') as f:
        for line in f:
            all_line += 1
            if line.strip():
                real_line += 1
                flname2 = flname.split('.')
                flname2[0] = f'{flname2[0]}-{real_line}'
                flname2 = '.'.join(flname2)
                
                hash_file = hashlib.md5()
                os.makedirs(os.path.dirname(f'/tmp/{flname2}'), exist_ok=True)
                with open(f'/tmp/{flname2}', 'w+') as ff:
                    ff.write(line)
                ff.close
                newpath = f'lines/{flname2}'
                s3.upload_file(Bucket=bucket, Key=newpath, Filename=f'/tmp/{flname2}')
                
                    
                with open(f'/tmp/{flname2}', 'rb') as ff2:
                    buf = ff2.read()
                    hash_file.update(bytes(buf.decode("utf-8").replace(' ',''), 'utf-8'))
                    xx = hash_file.hexdigest()
                    if xx in Hashes:
                        dupes.append(real_line)
                        dupes.append(Hashes.index(xx)+1)
                        print(f'Duplicate line is: {line}')
                    else:
                        write_line.append(line)
                    Hashes.append(xx)
                
                flname2 = flname.split('.')
                flname2[0] = f'{flname2[0]}-{real_line}-hash'
                flname2 = '.'.join(flname2)
                
                os.makedirs(os.path.dirname(f'/tmp/{flname2}'), exist_ok=True)
                with open(f'/tmp/{flname2}', 'w+') as ff_hash:
                    ff_hash.write(hash_file.hexdigest())
                ff_hash.close
                newpath = f'lines/{flname2}'
                s3.upload_file(Bucket=bucket, Key=newpath, Filename=f'/tmp/{flname2}')
    
    print("The identical lines are :")
    for x in dupes:
        flname2 = flname.split('.')
        flname2[0] = f'{flname2[0]}-{x}'
        flname2 = '.'.join(flname2)
        print(f'{flname2} , ')
    print(' \n')
    
    empty_line= all_line - real_line
    print(f'total lines = {all_line} \n')
    print(f'real lines = {real_line} \n')
    print(f'empty lines = {empty_line} \n')

    flname3 = flname.split('.')
    flname3[0] = f'{flname3[0]}-clean'
    flname3 = '.'.join(flname3)
    newpath2 = f'cleaned/{flname3}'
    
    os.makedirs(os.path.dirname(f'/tmp/{flname3}'), exist_ok=True)
    with open (f'/tmp/{flname3}', 'w+') as ff3:
        for x in write_line:
            ff3.write(f'{x} \n')
    s3.upload_file(Bucket=bucket, Key=newpath2, Filename=f'/tmp/{flname3}')
    
    print('THE LIST OF FILES BY SIZE : ')
    files = dict()
    for key in s3.list_objects(Bucket=bucket, Prefix='lines/')['Contents']:
        files[key['Key'].split('/')[-1]] = key['Size']

    sort_files = sorted(files.items(), key=lambda x: x[1], reverse=True)
    for i in sort_files:
        if i[0].split('.')[0].split('-')[-1] != 'hash':
            print(i[0], i[1])
       
    return event 