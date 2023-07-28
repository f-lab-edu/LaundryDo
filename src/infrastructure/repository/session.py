from src.domain import Clothes, User, Order, LaundryBag, Machine

session = {'clothes' : {'clothesid' : Clothes(clothesid,
                                                  label,
                                                  volume,
                                                  orderid,
                                                  laundrybagid,
                                                  status,
                                                  received_at
                                                  
                                                  )},
               'user' : {'userid' : User(address, userid, orderlist)},

               'order' : {'orderid' : Order(orderid, received_at, status, userid, clothes_list)},

               'laundrybag' : {'laundrybagid' : LaundryBag(laundrybagid, status, machineid, create_at, label, clothes_list)},

               'machine' : {'machineid' : Machine(machineid, contained, start_time, lastupdateTime, status)}

               }
    

class MapDict(dict) :
    def __init__(self) :
        super().__init__()

    def filter_by(self, **kwargs) :
        assert len(kwargs) == 1, 'filter_by function can work only one at a time.'
        [attrKey], [attrValue] = zip(*kwargs.items())
        return [v for v in self.values() if getattr(v, attrKey) == attrValue]

        # filter by
        # clothesid, status, 
        # 

class Session :

    def __init__(self) :
        self.buffers = {}
        self.map_dict = {
                         Clothes : MapDict(),
                         User : MapDict(),
                         Order : MapDict(),
                         LaundryBag : MapDict(),
                         Machine : MapDict()
                         }

    def query(self, obj) :
        self.map_dict[obj]

    def commit(self) :
        for buffer_key, buffer_values in self.buffers.items() :
            if buffer_key is Clothes :
            # clothes -> # clothes만 따로 들어오는 일은 없어야한다. clothes는 항상 order 단위로 input
                self.map_dict[buffer_key] self.buffer

            elif buffer_key is Order :
            # order -> user.orderlist

            elif buffer_key is LaundryBag :
            # laundrybag -> clothes.laundrybagid, clothes.status, clothes_list


            elif buffer_key is Machine :
            # machine -> laundrybag.machineid, clothes.state, laundrybag.status
    
    

    


        self.rollback()


    def rollback(self) :
        self.buffer = {}