import qrcode

def generate_qr(fruit_id:str , save_path: str = None):
    url = f"http://127.0.0.1:8000/history/{fruit_id}"
    qr = qrcode.make(url)

    if not save_path:
        save_path = f"{fruit_id}_qrcode.png"

    qr.save(save_path)
    return save_path

#Test
if __name__=="__main__":
    path = generate_qr("apple123")
    print(f"QR Code saved at {path}")