export interface AuthI {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface LoginI {
  username: string
  password: string
}
export interface RegisterI {
  username: string
  email: string
  password: string
  role: 'user' | 'admin'
}
