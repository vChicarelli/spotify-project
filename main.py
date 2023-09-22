from utils import Utils

sp = Utils()

x = -1 
while x != 0:
    print("===== M E N U =====")
    print("1- Verificar playlist")
    print("2- Procurar música")
    print("3- Testing")
    print("0- Sair")
    resp = input("Digite uma opção: ")
    if(resp == "1"):
        url = input("Insira o link da playlist: ")
        p_id = url.split("/")[-1].split("?")[0]
        sp.songs_playlist(p_id)
    if(resp == "2"):
        sp.search_song()
    if(resp == "3"):
        print(sp.playlist_id)
        sp.testing()
    if(resp == "0"):
        exit()