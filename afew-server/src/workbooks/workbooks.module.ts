import { Module } from '@nestjs/common';
import { WorkbooksService } from './workbooks.service';
import { WorkbooksController } from './workbooks.controller';

@Module({
  controllers: [WorkbooksController],
  providers: [WorkbooksService],
})
export class WorkbooksModule {}
