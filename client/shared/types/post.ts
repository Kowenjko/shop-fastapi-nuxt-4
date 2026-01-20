import type { MetaI } from './meta'
import type { UserI, ProfileI } from './user'

export interface PostCreateI {
  title: string
  content: string
  user_id: number
}

export interface PostI extends PostCreateI {
  id: number
  user: UserI
  profile: ProfileI
}

export interface PostsI {
  items: PostI[]
  meta: MetaI
}
