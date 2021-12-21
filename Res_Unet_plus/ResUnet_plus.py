import torch
import torch.nn as nn



class ResidualStem(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ResidualStem, self).__init__()

        self.conv_block1 = nn.Sequential(
            
            nn.Conv2d(input_dim, int(output_dim/2), kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(int(output_dim/2)),
            nn.ReLU(),
            nn.Conv2d(int(output_dim/2), int(output_dim/2), kernel_size=3, padding=1),
            nn.BatchNorm2d(int(output_dim/2))
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv2d(int(output_dim/2), output_dim, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(output_dim),
            nn.ReLU(),
            nn.Conv2d(output_dim, output_dim, kernel_size=3, padding=1),
            nn.BatchNorm2d(output_dim)
            )

        self.conv_skip = nn.Sequential(
            nn.Conv2d(int(output_dim/2), output_dim, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(output_dim)
        )

        self.relu = nn.ReLU(inplace=True)


    def forward(self, x):
        x1 = self.conv_block1(x)
        x2 = self.conv_block2(x1) + self.conv_skip(x1)
        x3 = self.relu(x2)
        return x3


class ResidualBlock(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ResidualBlock, self).__init__()

        self.conv_block1 = nn.Sequential(
            
            nn.Conv2d(input_dim, int(output_dim/2), kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(int(output_dim/2)),
            nn.ReLU(),
            nn.Conv2d(int(output_dim/2), int(output_dim/2), kernel_size=3, padding=1),
            nn.BatchNorm2d(int(output_dim/2))
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv2d(int(output_dim/2), output_dim, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(output_dim),
            nn.ReLU(),
            nn.Conv2d(output_dim, output_dim, kernel_size=3, padding=1),
            nn.BatchNorm2d(output_dim)
            )

        self.conv_skip = nn.Sequential(
            nn.Conv2d(int(output_dim/2), output_dim, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(output_dim)
        )

        self.relu = nn.ReLU(inplace=True)


    def forward(self, x):
        x1 = self.conv_block1(x)
        x2 = self.relu(x + x1)
        x3 = self.conv_block2(x2) + self.conv_skip(x2)
        x4 = self.relu(x3)
        return x4



class BasicConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, bias=True):
        super(BasicConv2d, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias)
        self.bn = nn.BatchNorm2d(out_channels, eps=0.001, momentum=0.1)
        self.relu = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x



class BridgeConv(nn.Module):

    def __init__(self, in_channels, out_channels):
        super(BridgeConv, self).__init__()

        # number of input channels is a number of filters in the previous layer
        # number of output channels is a number of filters in the current layer
        # "same" convolutions
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
            )

    def forward(self, x):
        x = self.conv(x)
        return x


class UpConv(nn.Module):

    def __init__(self, in_channels, out_channels):
        super(UpConv, self).__init__()

        self.up = nn.Sequential(
            nn.UpsamplingBilinear2d(scale_factor=2),
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.up(x)
        return x


class Upsample(nn.Module):
    def __init__(self, input_dim, output_dim, kernel, stride, padding):
        super(Upsample, self).__init__()

        self.upsample = nn.ConvTranspose2d(
            input_dim, output_dim, kernel_size=kernel, stride=stride, padding=padding)  

    def forward(self, x):
        return self.upsample(x)


class ResUnet_plus(nn.Module):
    def __init__(self, img_ch=3, output_ch=1):
        super(ResUnet_plus, self).__init__()

        self.encoder0 = ResidualStem(input_dim = img_ch, output_dim = 64)

        self.encoder1 = ResidualBlock(input_dim = 64, output_dim = 128)

        self.encoder2 = ResidualBlock(input_dim = 128, output_dim = 256)

        self.encoder3 = ResidualBlock(input_dim = 256, output_dim = 512)

        self.encoder4 = ResidualBlock(input_dim = 512, output_dim = 1024)

        self.encoder5 = BridgeConv(in_channels = 1024, out_channels = 2048)

        self.MaxPool = nn.MaxPool2d(kernel_size=3,stride=2,ceil_mode=True)

        self.UpConv5_4 = Upsample(2048, 1024, kernel=2, stride=2, padding=0)
        self.UpConv5_3 = Upsample(2048, 128, kernel=4, stride=4, padding=0)
        self.UpConv5_2 = Upsample(2048, 64, kernel=8, stride=8, padding=0)
        self.UpConv5_1 = Upsample(2048, 32, kernel=16, stride=16, padding=0)
        self.UpConv5_0 = Upsample(2048, 16, kernel=32, stride=32, padding=0)

        self.UpConv4_3 = Upsample(2048, 512, kernel=2, stride=2, padding=0)
        self.UpConv4_2 = Upsample(2048, 64, kernel=4, stride=4, padding=0)
        self.UpConv4_1 = Upsample(2048, 32, kernel=8, stride=8, padding=0)
        self.UpConv4_0 = Upsample(2048, 16, kernel=16, stride=16, padding=0)

        self.UpConv3_2 = Upsample(1152, 256, kernel=2, stride=2, padding=0)
        self.UpConv3_1 = Upsample(1152, 32, kernel=4, stride=4, padding=0)
        self.UpConv3_0 = Upsample(1152, 16, kernel=8, stride=8, padding=0)

        self.UpConv2_1 = Upsample(640, 128, kernel=2, stride=2, padding=0)
        self.UpConv2_0 = Upsample(640, 16, kernel=4, stride=4, padding=0)

        self.UpConv1_0 = Upsample(352, 64, kernel=2, stride=2, padding=0)


        self.decoder0 =  nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, output_ch, kernel_size=3, stride=1, padding=1)
            )



    def forward(self, x):
        
        # print("input: ", list(x.size()))
        # Encode

        e0 = self.encoder0(x)   # C*W*H 64*512*512

        maxpool0 = self.MaxPool(e0) 
        e1 = self.encoder1(maxpool0)   # C*W*H 128*256*256
        # print("encoder 1", list(e1.size()))

        maxpool1 = self.MaxPool(e1)   # C*W*H 128*128*128
        e2 = self.encoder2(maxpool1)  # C*W*H 256*128*128

        maxpool2 = self.MaxPool(e2)   # C*W*H 256*64*64
        e3 = self.encoder3(maxpool2)  # C*W*H 512*64*64

        maxpool3 = self.MaxPool(e3)   # C*W*H 512*32*32
        e4 = self.encoder4(maxpool3)  # C*W*H 1024*32*32
        
        maxpool4 = self.MaxPool(e4)   # C*W*H 1024*16*16
        e5 = self.encoder5(maxpool4)  # C*W*H 2048*16*16
        # print("bridge before attention",list(e5.size()))

        # Decode
        # print("bridge after attention", list(att_x5.size()))
        d5_4 = self.UpConv5_4(e5)   # C*W*H 1024*32*32
        d5_3 = self.UpConv5_3(e5)   # C*W*H 128*64*64
        d5_2 = self.UpConv5_2(e5)   # C*W*H 64*128*128
        d5_1 = self.UpConv5_1(e5)   # C*W*H 32*256*256
        d5_0 = self.UpConv5_0(e5)   # C*W*H 16*512*512
        # print("after decoding 5",list(d5.size()))
        # print("after encoding 4",list(e4.size()))

        d4 = torch.cat((e4, d5_4), dim=1)  # C*W*H 2048*32*32
        d4_3 = self.UpConv4_3(d4)          
        d4_2 = self.UpConv4_2(d4)
        d4_1 = self.UpConv4_1(d4)
        d4_0 = self.UpConv4_0(d4)


        d3 = torch.cat((e3, d5_3, d4_3), dim=1)  # C*W*H 1152*64*64
        d3_2 = self.UpConv3_2(d3)           
        d3_1 = self.UpConv3_1(d3)
        d3_0 = self.UpConv3_0(d3)


        d2 = torch.cat((e2, d5_2, d4_2, d3_2), dim=1)  # C*W*H 640*128*128
        d2_1 = self.UpConv2_1(d2)            
        d2_0 = self.UpConv2_0(d2)   


        d1 = torch.cat((e1, d5_1, d4_1, d3_1, d2_1), dim=1)  # C*W*H 352*256*256
        d0 = self.UpConv1_0(d1)            

        output = self.decoder0(d0)   # C*W*H output_ch*512*512

        return output
