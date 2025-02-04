import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

def model_cheese():
    cheese = pd.read_csv("com_cheese_api/resources/data/cheese_dataset.csv")
    cheese_matching = pd.read_csv("com_cheese_api/resources/data/cheese_matching.csv", encoding="utf-8")

    cheese_df = cheese.rename(columns = {"Unnamed: 0": "cheese_no"})
    cheese_matching_df = cheese_matching.rename(columns={"Unnamed: 0": "cheese_no"})

    cheese_data = pd.merge(cheese_df, cheese_matching_df, on="cheese_no", how = "inner")

    cheese_model_data = cheese_data.drop(['Unnamed: 0.1', 'content', 'img', 'brand', 'country', 'matching'], axis = 1)
    cheese_2 = cheese_data.drop(['Unnamed: 0.1', 'content', 'img', 'matching'], axis = 1)
    # cheese_model_data.to_csv("resources/data/cheese_model_data.csv", encoding = 'utf-8-sig')

    # print('cheese_model_data: ', {cheese_model_data})
    # print()

    X_cheese = cheese_model_data.iloc[:, 3:68]
    # X_cheese = X_cheese.drop(['name', 'category', 'texture', 'types', 'price', 'brand_code', 'country_code'], axis = 1)
    X_cheese = X_cheese.drop(['name', 'category', 'types', 'price'], axis = 1)
    y_cheese = cheese_model_data[['category']]
    # y_cheese = cheese_model_data[['name']]

    X_cheese_train, X_cheese_test, y_cheese_train, y_cheese_test = train_test_split(X_cheese, y_cheese, test_size = 0.3)

    # X_cheese_sc = StandardScaler().fit_transform(X_cheese)
    # X_cheese_train_sc = StandardScaler().fit_transform(X_cheese_train)
    # X_cheese_test_sc = StandardScaler().fit_transform(X_cheese_test)

    # features = ['texture', 'types',
    #     'price', 'brand_code', 'country_code', '간식', '감자', '견과류', '과일', '그라탕',
    #     '김가루', '꿀', '딥소스', '라자냐', '리소토', '마르게리타 피자', '막걸리', '맥앤치즈', '맥주',
    #     '멤브리요', '무화과', '바질', '발사믹 식초', '발사믹식초', '배', '베이컨', '볶음밥', '비스킷', '빵',
    #     '사케', '사퀘테리', '샌드위치', '샐러드', '샐러리', '샤퀴테리', '소금', '스테이크', '스프', '스프레드',
    #     '올리브오일', '올리브유', '와인', '위스키', '잼', '채소', '치즈케이크', '카나페', '카프레제',
    #     '카프레제 샐러드', '크래커', '크로스티니', '키쉬', '타르트', '타파스', '테이블치즈', '토마토', '토스트',
    #     '파스타', '팬케이크', '퐁듀', '피자', '핑거 푸드', '핑거푸드', '화이트와인']

    X_cheese_train = X_cheese_train.astype('float32')
    X_cheese_test = X_cheese_test.astype('float32')
    print(X_cheese_train.shape)
    model = tf.keras.models.Sequential([       # valid (default 값)
        tf.keras.layers.Dense(128, activation='relu', input_dim=61),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(64, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

    model.fit(X_cheese_train, y_cheese_train, batch_size=10, validation_data=(X_cheese_test, y_cheese_test), epochs=300)

    loss, acc = model.evaluate(X_cheese_test, y_cheese_test, batch_size=10)

    print('loss: ', loss)
    print('acc: ', acc)

if __name__ == '__main__':
    model = model_cheese()
    # model.save("mymodel.h5")
