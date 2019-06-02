def get_user_avatar(message, args):
    """Retrieve avatar for provided user."""
    name = str(args.lower())
    msg = "http://fp.chatango.com/profileimg/" \
        + name[0] + "/" \
        + name[1] + "/" \
        + name + "/full.jpg"
    return msg
