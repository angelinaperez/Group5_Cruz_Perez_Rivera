from windows import *

root = Tk()
# MAIN MENU
add_product = Button(root, width=15, bd=3,
                     text="List of Products", font=times_new_roman,
                     bg="pink",
                     command=ListOfProduct)
add_stock = Button(root, width=15, bd=3,
                   text="Add Stock", font=times_new_roman,
                   bg="pink",
                   command=AddStock)
sell_product = Button(root, width=15, bd=3,
                      text="Sales", font=times_new_roman,
                      bg="pink",
                      command=Sales)
view_inventory = Button(root, width=15, bd=3,
                        text="View Inventory", font=times_new_roman,
                        bg="pink",
                        command=Inventory)

add_product.grid()
add_stock.grid()
sell_product.grid()
view_inventory.grid()

root.title("CROCHET SHOP INVENTORY")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.mainloop()
