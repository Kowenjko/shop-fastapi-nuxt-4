export interface UserI {
  id: number
  username: string
  email: string
  active: boolean
  role: 'user' | 'admin'
}
