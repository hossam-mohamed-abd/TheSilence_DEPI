import bcrypt from "bcryptjs";
import authRepository from "./auth.repository";
import { RegisterDto, LoginDto } from "./auth.types";
import { generateToken } from "../../utils/generateToken";
import { NotificationService } from "../notifications/notification.service";
class AuthService {
  private notificationService = new NotificationService();

  async register(data: RegisterDto) {
    const user = await authRepository.findByEmail(data.email);

    if (user) {
      throw new Error("Email already exists");
    }

    const hashedPassword = await bcrypt.hash(data.password, 10);

    const newUser = await authRepository.create({
      first_name: data.firstName,
      last_name: data.lastName,
      email: data.email,
      password_hash: hashedPassword,
      phone: data.phone,
      role: "customer",
      is_active: true,
      cities: {
        connect: {
          id: BigInt(data.cityId),
        },
      },
    });

    // 🔔 Welcome Notification
    await this.notificationService.createWelcomeNotification(newUser.id);

    const token = generateToken(newUser.id);

    return {
      user: newUser,
      token,
    };
  }

  async login(data: LoginDto) {
    const user = await authRepository.findByEmail(data.email);

    if (!user) {
      throw new Error("Invalid email or password");
    }

    const isPasswordCorrect = await bcrypt.compare(
      data.password,
      user.password_hash!,
    );

    if (!isPasswordCorrect) {
      throw new Error("Invalid email or password");
    }

    const token = generateToken(user.id);

    return {
      user,
      token,
    };
  }

  async profile(userId: number) {
    const user = await authRepository.findById(BigInt(userId));

    if (!user) {
      throw new Error("User not found");
    }

    return user;
  }
}

export default new AuthService();
