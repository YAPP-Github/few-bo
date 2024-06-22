import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { WorkbooksModule } from './workbooks/workbooks.module';
import { ArticlesModule } from './articles/articles.module';
import { UsersModule } from './users/users.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      cache: true,
      isGlobal: true,
    }),
    MongooseModule.forRoot('mongodb://localhost/nest'),
    WorkbooksModule, 
    ArticlesModule, 
    UsersModule
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

// mongodb+srv://admin:<password>@cluster0.lkxrrhr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0