from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

# Create your views here.

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def diffie_hellman(request):
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
    a_private_key = parameters.generate_private_key()
    a_peer_public_key = a_private_key.public_key()

    b_private_key = parameters.generate_private_key()
    b_peer_public_key = b_private_key.public_key()

    a_shared_key = a_private_key.exchange(b_peer_public_key)
    b_shared_key = b_private_key.exchange(a_peer_public_key)

    return render(request, "app4/DiffieHellman.html", {"a_shared_key": a_shared_key, "b_shared_key": b_shared_key })