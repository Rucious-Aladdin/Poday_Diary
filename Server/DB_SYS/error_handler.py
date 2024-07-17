import pandas as pd
import os

class ErrorHandler:
    ## 이미 유저가 존재하는 경우 user_already_exist 에러 raise
    def user_already_exist_error(self):
        self.user_create = False
        print(f"{self.user_id}는 이미 존재하는 유저입니다.")
    
    ## data.csv 파일이 존재하지 않을때 생성.
    def handle_df_not_found_error(self, filename="data.csv"):
        print("db_file is creating... " + "path: " + str(os.path.join(self.text_path, filename)))
        initial_df = pd.DataFrame(columns=["date", "diary", "diary_title", "conversations", "emotion", "img_prompt", "img_filename", "song_indices", "book_indices"])
        initial_df.to_csv(os.path.join(self.text_path, filename), index=False, sep="\t")
        self.user_create = True
        return initial_df
    
    ## delete시에 해당하는 행이 없는 경우 ValueError Raise
    def target_row_not_found_error(self , date):
        print(f"{self.user_id} 유저의 DB내에 날짜: {date}에 해당하는 행이 없습니다.")
        self.found_row = False
    