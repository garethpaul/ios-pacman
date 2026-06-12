//
//  APPViewController.m
//

#import "APPViewController.h"

@interface APPViewController ()

@end

@implementation APPViewController

- (void)viewDidLoad {
    
    [super viewDidLoad];
    
    // Animate ghosts
    
    CGPoint origin1 = self.ghost1.center;
    CGPoint target1 = CGPointMake(self.ghost1.center.x, self.ghost1.center.y-124);
    CABasicAnimation *bounce1 = [CABasicAnimation animationWithKeyPath:@"position.y"];
    bounce1.duration = 2;
    bounce1.fromValue = [NSNumber numberWithInt:origin1.y];
    bounce1.toValue = [NSNumber numberWithInt:target1.y];
    bounce1.repeatCount = HUGE_VALF;
    bounce1.autoreverses = YES;
    [self.ghost1.layer addAnimation:bounce1 forKey:@"position"];
    
    CGPoint origin2 = self.ghost2.center;
    CGPoint target2 = CGPointMake(self.ghost2.center.x, self.ghost2.center.y+284);
    CABasicAnimation *bounce2 = [CABasicAnimation animationWithKeyPath:@"position.y"];
    bounce2.fromValue = [NSNumber numberWithInt:origin2.y];
    bounce2.toValue = [NSNumber numberWithInt:target2.y];
    bounce2.duration = 2;
    bounce2.repeatCount = HUGE_VALF;
    bounce2.autoreverses = YES;
    [self.ghost2.layer addAnimation:bounce2 forKey:@"position"];
    
    CGPoint origin3 = self.ghost3.center;
    CGPoint target3 = CGPointMake(self.ghost3.center.x, self.ghost3.center.y-284);
    CABasicAnimation *bounce3 = [CABasicAnimation animationWithKeyPath:@"position.y"];
    bounce3.fromValue = [NSNumber numberWithInt:origin3.y];
    bounce3.toValue = [NSNumber numberWithInt:target3.y];
    bounce3.duration = 2;
    bounce3.repeatCount = HUGE_VALF;
    bounce3.autoreverses = YES;
    [self.ghost3.layer addAnimation:bounce3 forKey:@"position"];
    
    // Movement of pacman
    
    self.lastUpdateTime = [[NSDate alloc] init];
        
    self.currentPoint  = CGPointMake(0, 144);
    self.previousPoint = self.currentPoint;
    self.motionManager = [[CMMotionManager alloc]  init];
    self.queue         = [[NSOperationQueue alloc] init];
    
    self.motionManager.accelerometerUpdateInterval = kUpdateInterval;

    __weak APPViewController *weakSelf = self;
    [self.motionManager startAccelerometerUpdatesToQueue:self.queue withHandler:
     ^(CMAccelerometerData *accelerometerData, NSError *error) {
         if (error != nil || accelerometerData == nil) {
             return;
         }
         APPViewController *strongSelf = weakSelf;
         if (strongSelf == nil) {
             return;
         }
         strongSelf.acceleration = accelerometerData.acceleration;
         [strongSelf performSelectorOnMainThread:@selector(update) withObject:nil waitUntilDone:NO];
     }];

}

- (void)movePacman {
    // Resolve physical constraints before evaluating gameplay outcomes.
    [self collisionWithBoundaries];
    [self collisionWithWalls];

    CGRect candidateFrame = [self candidatePacmanFrame];
    [self collisionWithExit:candidateFrame];
    if (!self.gameCompleted) {
        [self collisionWithGhosts:candidateFrame];
    }

    // Move pacman to its new position

    self.pacman.frame = [self candidatePacmanFrame];
    
    // Rotate the sprite
    
    CGFloat newAngle = (self.pacmanXVelocity + self.pacmanYVelocity) * M_PI * 4;
    self.angle += newAngle * kUpdateInterval;
    
    CABasicAnimation *rotate;
    rotate                     = [CABasicAnimation animationWithKeyPath:@"transform.rotation"];
    rotate.fromValue           = [NSNumber numberWithFloat:0];
    rotate.toValue             = [NSNumber numberWithFloat:self.angle];
    rotate.duration            = kUpdateInterval;
    rotate.repeatCount         = 1;
    rotate.removedOnCompletion = NO;
    rotate.fillMode            = kCAFillModeForwards;
    [self.pacman.layer addAnimation:rotate forKey:@"10"];
    
    // Save previous position
    
    self.previousPoint = self.currentPoint;

}

- (CGRect)candidatePacmanFrame {
    CGRect frame = self.pacman.frame;
    frame.origin = self.currentPoint;
    return frame;
}

- (void)collisionWithExit:(CGRect)pacmanFrame {

    if (CGRectIntersectsRect(pacmanFrame, self.exit.frame)) {
        if (self.collisionAlertVisible) {
            return;
        }
        
        self.gameCompleted = YES;
        self.pacmanXVelocity = 0;
        self.pacmanYVelocity = 0;
        [self.motionManager stopAccelerometerUpdates];
        self.collisionAlertVisible = YES;
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Congratulations"
                                                        message:@"You've won the game!"
                                                       delegate:self
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
    
    }
    
}

- (void)collisionWithGhosts:(CGRect)pacmanFrame {

    CALayer *ghostLayer1 = (CALayer *)self.ghost1.layer.presentationLayer ?: self.ghost1.layer;
    CALayer *ghostLayer2 = (CALayer *)self.ghost2.layer.presentationLayer ?: self.ghost2.layer;
    CALayer *ghostLayer3 = (CALayer *)self.ghost3.layer.presentationLayer ?: self.ghost3.layer;

    if (CGRectIntersectsRect(pacmanFrame, ghostLayer1.frame)
        || CGRectIntersectsRect(pacmanFrame, ghostLayer2.frame)
        || CGRectIntersectsRect(pacmanFrame, ghostLayer3.frame) ) {
        if (self.collisionAlertVisible) {
            return;
        }
    
        self.currentPoint  = CGPointMake(0, 144);
        self.pacmanXVelocity = 0;
        self.pacmanYVelocity = 0;
        self.collisionAlertVisible = YES;
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Oops!"
                                                  message:@"Mission Failed!"
                                                  delegate:self
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles:nil];
        [alert show];
        
    }
    
}


- (void)collisionWithBoundaries {

    if (self.currentPoint.x < 0) {
        _currentPoint.x = 0;
        self.pacmanXVelocity = -(self.pacmanXVelocity / 2.0);
    }
    
    if (self.currentPoint.y < 0) {
        _currentPoint.y = 0;
        self.pacmanYVelocity = -(self.pacmanYVelocity / 2.0);
    }
    
    if (self.currentPoint.x > self.view.bounds.size.width - self.pacman.image.size.width) {
        _currentPoint.x = self.view.bounds.size.width - self.pacman.image.size.width;
        self.pacmanXVelocity = -(self.pacmanXVelocity / 2.0);
    }
    
    if (self.currentPoint.y > self.view.bounds.size.height - self.pacman.image.size.height) {
        _currentPoint.y = self.view.bounds.size.height - self.pacman.image.size.height;
        self.pacmanYVelocity = -(self.pacmanYVelocity / 2.0);
    }
    
}

- (void)collisionWithWalls {
    CGRect frame = [self candidatePacmanFrame];
    
    for (UIImageView *image in self.wall) {
    
        if (CGRectIntersectsRect(frame, image.frame)) {
        
            // Compute collision angle
            CGPoint pacmanCenter = CGPointMake(frame.origin.x + (frame.size.width / 2),
                                               frame.origin.y + (frame.size.height / 2));
            CGPoint imageCenter  = CGPointMake(image.frame.origin.x + (image.frame.size.width / 2),
                                               image.frame.origin.y + (image.frame.size.height / 2));
            CGFloat angleX = pacmanCenter.x - imageCenter.x;
            CGFloat angleY = pacmanCenter.y - imageCenter.y;
                
            if (fabs(angleX) > fabs(angleY)) {
                _currentPoint.x = self.previousPoint.x;
                self.pacmanXVelocity = -(self.pacmanXVelocity / 2.0);
            } else {
                _currentPoint.y = self.previousPoint.y;
                self.pacmanYVelocity = -(self.pacmanYVelocity / 2.0);
            }
        
       }
    
    }
    
}

- (void)update {
    if (self.collisionAlertVisible || self.gameCompleted) {
        return;
    }
    
    NSTimeInterval secondsSinceLastDraw = -([self.lastUpdateTime timeIntervalSinceNow]);
    secondsSinceLastDraw = MAX(0, MIN(secondsSinceLastDraw, 0.1));
        
    self.pacmanYVelocity = self.pacmanYVelocity - (self.acceleration.x * secondsSinceLastDraw);
    self.pacmanXVelocity = self.pacmanXVelocity - (self.acceleration.y * secondsSinceLastDraw);
        
    CGFloat xDelta = secondsSinceLastDraw * self.pacmanXVelocity * 500;
    CGFloat yDelta = secondsSinceLastDraw * self.pacmanYVelocity * 500;
        
    self.currentPoint = CGPointMake(self.currentPoint.x + xDelta,
                                    self.currentPoint.y + yDelta);
        
    [self movePacman];
    
    self.lastUpdateTime = [NSDate date];
    
}

- (void)alertView:(UIAlertView *)alertView didDismissWithButtonIndex:(NSInteger)buttonIndex
{
    self.collisionAlertVisible = NO;
    self.lastUpdateTime = [NSDate date];
}

- (void)dealloc
{
    [self.motionManager stopAccelerometerUpdates];
}

@end
