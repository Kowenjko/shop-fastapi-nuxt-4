import type { CityI } from './city'

export interface UserI {
  id: number
  username: string
  email: string
  active: boolean
  role: 'user' | 'admin'
}
export interface ProfileI {
  id: number
  first_name: string
  last_name: string
  phone: string
  city_id: string
  age: number
  user: UserI
  city: CityI
}
