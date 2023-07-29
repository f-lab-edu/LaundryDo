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

## should care about the primary key instead of {object}id
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
            
            self.map_dict[buffer_key].update(buffer_dict)
            # clothes -> # clothes만 따로 들어오는 일은 없어야한다. clothes는 항상 order 단위로 input
            if buffer_key is Clothes :
                continue

            # order -> user.orderlist
            # order -> clothes_list
            elif buffer_key is Order :
                # update order
                
                for order in buffer_dict.values() :
                    # update clothes
                    self.update_clothes_from_order(order)
                    # update user
                    self.update_user_from_order(order)
                    
            

            elif buffer_key is LaundryBag :

                for laundrybag in buffer_dict.values() :
                    # update clothes
                    self.update_clothes_from_laundrybag(laundrybag)
                    
            # laundrybag -> clothes.laundrybagid, clothes.status, clothes_list


            elif buffer_key is Machine :
                for machine in buffer_dict.values() :
                    # update clothes
                    self.update_clothes_from_machine(machine)
                    # update laundrybag 
                    self.update_laundrybag_from_machine(machine)
                    # update order
                    self.update_order_from_machine(machine)
                
            # machine -> laundrybag.machineid, clothes.state, laundrybag.status
    

        self.rollback()

    def update_clothes_from_order(self, order : Order) :
        self.map_dict[Clothes].update({clothes.clothesid : clothes for clothes in order.clothes_list})

    def update_user_from_order(self, order : Order) :
        pass

    def update_clothes_from_laundrybag(self, laundrybag : LaundryBag) :
        self.map_dict[Clothes].update({clothes.clothesid : clothes for clothes in laundrybag.clothes_list})

    def update_clothes_from_machine(self, machine : Machine) :
        self.map_dict[Clothes].update({clothes.clothesid : clothes for clothes in machine.contained.clothes_list})

    def update_laundrybag_from_machine(self, machine : Machine) :
        self.map_dict[LaundryBag].update({machine.contained.laundrybagid : machine.contained})

    def update_order_from_machine(self, machine) :
        pass





    def rollback(self) :
        self.buffers = {
                         Clothes : MapDict(),
                         User : MapDict(),
                         Order : MapDict(),
                         LaundryBag : MapDict(),
                         Machine : MapDict()
                         }