import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { WorkbookModule } from './workbook/workbook.module';
import { ArticleModule } from './article/article.module';
import { ProblemModule } from './problem/problem.module';
import { UserModule } from './user/user.module';

@Module({
  imports: [WorkbookModule, ArticleModule, ProblemModule, UserModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
