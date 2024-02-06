GallowsGame.game();
class GallowsGame{
    public static void game(){
        start_request();
        string? riddle;
        string? hint;
        word_request(out riddle, out hint);
        guess_request(hint, riddle);
        guessing(riddle);
    }


    public static void start_request(){
        Console.WriteLine("Вы готовы??\nНапишите 'Yes', если да и 'No', если нет.");
        string? answer = Console.ReadLine();
        switch(answer){
            case "Yes":
                break;
            case "No":
                Console.WriteLine("До новых встреч!");
                Environment.Exit(0);
                break;
        }
    }


    public static void word_request(out string? riddle, out string? hint){
        Console.WriteLine("Введи слово, которое хотите загадать:");
        riddle = Console.ReadLine();
        Console.WriteLine("Введи 1 слово - подсказку:");
        hint = Console.ReadLine();
        Console.Clear();
    }


    public static void guess_request(string? hint, string? riddle){
        Console.WriteLine("Отгадай слово, загаданное другим игроком, чтобы спасти самоубийцу!");
        Console.WriteLine("Учти, что если допустишь 6 ошибок, человек погибнет!");
        Console.WriteLine($"Подсказка: {hint}");
        int l = riddle.Length;
    } 


    public static void guessing(string? riddle){
        string word = "";
        int mistakes = 0;
        int l = riddle.Length;
        string showing_word = string.Join("",Enumerable.Repeat(" _ ",l));
        while (mistakes < 6 & word.Length != riddle.Length){
            Console.WriteLine("\n" +showing_word);
            Console.WriteLine("Введи букву, которая по твоему мнению есть в загаданном слове!");
            switch (mistakes){
                case 0 or 5:
                    Console.WriteLine($"Ты допустил {mistakes} ошибок!");
                    break;
                case 1:
                    Console.WriteLine($"Ты допустил {mistakes} ошибку!");
                    break;
                case 2 or 3 or 4:
                    Console.WriteLine($"Ты допустил {mistakes} ошибки!");
                    break;
            }
            var inputing_letter = Console.ReadKey();
            if (riddle.Contains(inputing_letter.KeyChar)){
                int c = riddle.Count(ch => ch == inputing_letter.KeyChar);
                string additional_str = string.Join("",Enumerable.Repeat($"{inputing_letter.KeyChar}",c));  
                word += additional_str;
                for (int i = 0; i < riddle.Length;i++){
                    if (inputing_letter.KeyChar == riddle[i]){
                        showing_word = showing_word.Remove(i*3+1, 1).Insert(i*3+1,inputing_letter.KeyChar.ToString());
                    }
                }
                }
            else{
                mistakes ++;
                };
        if(mistakes == 6){
            Console.WriteLine("Ты не смог спасти его!");
            end();
        }
        if (word.Length == riddle.Length){
            Console.WriteLine($"\n{showing_word}\nТы спас его!");
            end();
        }
        }
        }


    public static void end(){
        Console.WriteLine("Хотите сыграть еще раз\nНапишите 'Yes', если да и 'No', если нет!");
        string? answer = Console.ReadLine();
        switch (answer){
            case "Yes":
                Console.Clear();
                game();
                break;
            case "No":
                Console.Clear();
                Console.WriteLine("Спасибо за игру!");
                Environment.Exit(0);
                break;
        }
    }
    }
