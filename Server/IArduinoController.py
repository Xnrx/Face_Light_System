class IArduinoController:
    def send_signal(self, signal):
        """
        向Arduino板发送信号。
        :param encode: 译码格式。
        """
        pass

    def receive_signal(self, encode):
        """
        接收Arduino板发来的信号。
        :param encode: 译码格式。
        """
        pass