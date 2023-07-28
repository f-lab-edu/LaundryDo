from src.domain import Clothes, User, Order, LaundryBag, Machine, ClothesState


'''
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
''' 

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

class FakeSession :

    def __init__(self) :
        self.buffers = {
                         Clothes : MapDict(),
                         User : MapDict(),
                         Order : MapDict(),
                         LaundryBag : MapDict(),
                         Machine : MapDict()
                         }
        self.map_dict = {
                         Clothes : MapDict(),
                         User : MapDict(),
                         Order : MapDict(),
                         LaundryBag : MapDict(),
                         Machine : MapDict()
                         }

    def query(self, obj) :
        return self.map_dict[obj]

    def commit(self) :
        for buffer_key, buffer_dict in self.buffers.items() :

            # clothes -> # clothes만 따로 들어오는 일은 없어야한다. clothes는 항상 order 단위로 input
            if buffer_key is Clothes :
            
                self.map_dict[buffer_key].update(buffer_dict)

            # order -> user.orderlist
            # order -> clothes_list
            elif buffer_key is Order :
                # update order
                self.map_dict[buffer_key].update(buffer_dict)
                for order in buffer_dict.values() :
                    # update clothes
                    self.update_clothes_from_order(order)
                    # update user
                    self.update_user_from_order(order)
                    
            

            elif buffer_key is LaundryBag :
                continue
            # laundrybag -> clothes.laundrybagid, clothes.status, clothes_list


            elif buffer_key is Machine :
                continue
            # machine -> laundrybag.machineid, clothes.state, laundrybag.status
    

        self.rollback()

    def update_clothes_from_order(self, order : Order) :
        # clothes.state
        # add clothesrepo
        # received_at
        tmp_dict = {}
        for clothes in order.clothes_list :
            clothes.status = ClothesState.PREPARING
            clothes.received_at = order.received_at
            tmp_dict[clothes.clothesid] = clothes
            
        self.map_dict[Clothes].update(tmp_dict)

    def update_user_from_order(self, order : Order) :
        pass

    def rollback(self) :
        self.buffers = {
                         Clothes : MapDict(),
                         User : MapDict(),
                         Order : MapDict(),
                         LaundryBag : MapDict(),
                         Machine : MapDict()
                         }