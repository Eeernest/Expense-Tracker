from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Security:
  @staticmethod
  def get_password_hash(password):
    return password_hash.hash(password)