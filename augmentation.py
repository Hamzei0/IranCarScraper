import os
import cv2 as cv

for car_name in os.listdir("dataset"):

    os.makedirs(f"dataset_augmented/flip/{car_name}", exist_ok=True)
    os.makedirs(f"dataset_augmented/rotate/{car_name}", exist_ok=True)

    for file_name in os.listdir(f"dataset/{car_name}"):
        if file_name.endswith(".jpg"):

            img = cv.imread(f"dataset/{car_name}/{file_name}")
            new_name = file_name.replace(".jpg", "")

            # اینه ای کردن عکس ها
            flip = cv.flip(img, 1)
            cv.imwrite(f"dataset_augmented/flip/{car_name}/{new_name}_flip.jpg", flip)

            # چرخش ۹۰ درجه عکسها
            rotate = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
            cv.imwrite(
                f"dataset_augmented/rotate/{car_name}/{new_name}_rotate.jpg", rotate
            )
    print(f"{car_name}: done")

print("finished !!!")
