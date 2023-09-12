## LaundryDo
설명 : 빨래 대행 서비스  

## TODO
- [ ] 코드 리뷰가 필요한 부분 이슈로 정리하기
- [ ] pydantic model
  - [ ] define request, response
  - [ ] validation
- [ ] apscheduler
- [ ] authentication
- [ ] make it async
  - [ ] async functions
  - [ ] async database
- [ ] deployment settings 
    - [ ] gunicorn w/ uvicorn [link](https://fastapi.tiangolo.com/deployment/server-workers/?h=uvicorn)



### 어플리케이션 프로세스
![프로세스](<img/LaundryDO full process.png>)
---

### 개발 프로세스
![구상도](<img/LaundryDo Diagram.png>)
---
### ERD
![ERD](<img/LaundryDo_schema_diagram.png>)


### 아키텍쳐
![architecture](<img/LaundryDo_arcitecture_diagram.png>)

### 도메인 레이어
![domain](<img/LaundryDo_domain_diagram.png>)

### 서비스 레이어
![service](<img/LaundryDo_service_layer_diagram.png>)


## API 엔트리포인트
![api entrypoint](<img/LaundryDo_api_definition.png>)


## Getting Started
```
make build
```

```
make c_up
```





- **user**
    
    ⇒ authentication
    
    - create_user : `POST`
    - delete_user : `DELETE`
    - update_user : `PUT`
    - user_list : `GET`
- **clothes**
    - request_status : `GET`
    
    label, volume  
    
    - create_clothes : `POST`
    - update_clothes : `POST`
    - delete_clothes : `POST`
- **order**
    - request_order : `POST`
    - update_order : `PUT` . clothes 추가, 변경, 삭제 path로 이동. ← 맨 마지막에
    - cancel_order : `POST`
    - request_order_status : `GET`
    - order_list : `GET`
- **laundrybag X**
- **machine (From Laundry Manager)**
    - check_machine_status : `GET`

## FastAPI Pydantic Model 설정

*각 endpoint의 Input, output에 필요한 모델들이 다를 수 있음.  

### User

- validation
    - userid
- authentication

| User | attributes | Usage |
| --- | --- | --- |
| UserBase | [userid] | delete_user, user_list |
| UserCreate | [userid, password, address] | create_user, update_user |

| Clothes | attributes | Usage |
| --- | --- | --- |
| ClothesBase | [label, orderid, volume] | create_clothes, update_clothes, delete_clothes |
| ClothesOut | [label, orderid, volume, status, received_at] | request_status |

| Order | attributes | Usage |
| --- | --- | --- |
| OrderCreate | [clothes_list, userid, received_at] | request_order, update_order, cancel_order |
| OrderOut | [clothes_list, userid, received_at, status] | request_order_status, order_list |

| Machine | attributes | Usage |
| --- | --- | --- |
| Machine | [machineid, status, lastupdateTime] | check_machine_status |