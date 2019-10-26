def get_user_avatar(message, args):
    """Retrieve avatar for provided user."""
    name = str(args.lower())
    msg = f"http://fp.chatango.com/profileimg/{name[0]}/{name[1]}/{name}/full.jpg"
    print(msg)
    return msg
