export interface RegisterDto {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  phone: string;
  cityId: number;
}

export interface LoginDto {
  email: string;
  password: string;
}
