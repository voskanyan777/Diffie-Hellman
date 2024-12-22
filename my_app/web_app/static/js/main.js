class DHAlgorithm {
    constructor() {
        this.p = BigInt("0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF");
        this.g = 2n;
        this.client_private_a = this.getRandomBigInt(1n, this.p - 1n);  // a
        this.shared_private_key = null;  // K
        this.client_public_key = null;  // A
    }

    getRandomBigInt(min, max) {
        const range = max - min + 1n;
        const randomValue = BigInt(Math.floor(Math.random() * Number(range)));
        return min + (randomValue % range);
    }

    modExp(base, exp, mod) {
        let result = 1n;
        base = base % mod;
        while (exp > 0n) {
            if (exp % 2n === 1n) {
                result = (result * base) % mod;
            }
            exp = exp / 2n;
            base = (base * base) % mod;
        }
        return result;
    }

    public_key() {
        this.client_public_key = this.modExp(this.g, this.client_private_a, this.p);
    }

    shared_key() {
        return this.shared_private_key;
    }
    set_shared_key(server_public_key) {
        this.shared_private_key = this.modExp(server_public_key, this.client_private_a, this.p);
    }
}

export const dh = new DHAlgorithm();

document.addEventListener('DOMContentLoaded', function() {
    // Вычисление публичного ключа клиента
    dh.public_key();
    // console.log(dh.client_public_key);
    // console.log(dh.client_public_key.toString());
    fetch('http://localhost:8000/public-keys/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({public_key: dh.client_public_key.toString()})  // Сериализуем как обычный объект
    })
    .then(response => response.json())
    .then(data => {
        const public_key = BigInt(data.public_key.toString());  // Преобразуем обратно в BigInt
        dh.set_shared_key(public_key)
        console.log(`SHARED PRIVATE KEY: ${dh.shared_key()}`)
        // Сохраняем общий ключ в localstorage
        localStorage.setItem("shared_private_key", dh.shared_key())
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

    var encryptedUsername = CryptoJS.AES.encrypt("HELLO WORLD", "321");
    console.log("Encrypted message: ", encryptedUsername.toString());

});

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


