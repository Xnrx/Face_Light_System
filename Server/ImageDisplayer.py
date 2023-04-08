import cv2


class ImageDisplayer:
    def display_image(self, image):
        """
        显示图像。
        :param image: 要显示的图像。
        """
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
