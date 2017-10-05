from ..common import initial_environment_config
from ..common.config import TrainingConfig

import glob
import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

REQUIRED_COLUMNS = ['categorical_accuracy', 'epoch', 'f1', 'loss', 'val_categorical_accuracy', 'val_f1', 'val_loss']


def plot():
    for history_file in list_training_folders():
        with open(history_file) as f:
            plot_csv_file(csv.reader(f), history_file)


def list_training_folders():
    return glob.glob(os.path.join(TrainingConfig.PATHS['MODELS'], '**', '*.csv'))


def plot_csv_file(reader, path):
    categories = []
    loss = []
    loss_val = []
    accuracy = []
    accuracy_val = []
    f1 = []
    f1_val = []
    nb_epochs = 0
    for i, row in enumerate(reader):

        if i == 0:
            if any([column_name not in row for column_name in REQUIRED_COLUMNS]):
                return
            categories.extend(row)
        else:
            nb_epochs += 1
            accuracy.append(float(row[1]))
            f1.append(float(row[2]))
            loss.append(float(row[3]))
            accuracy_val.append(float(row[4]))
            f1_val.append(float(row[5]))
            loss_val.append(float(row[6]))
    if len(loss) != 0 and len(loss_val) != 0:
        save_path = os.path.dirname(path)
        plot_data([loss, loss_val], 'Loss', os.path.join(save_path, 'loss.png'), 'loss')
        plot_data([accuracy, accuracy_val], 'Accuracy', os.path.join(save_path, 'accuracy.png'), 'accuracy')
        plot_data([f1, f1_val], 'F1 score', os.path.join(save_path, 'f1.png'), 'f1 score')
        with open(os.path.join(save_path, 'stats.csv'), 'w') as f:
            f.write('epoch,name,value\n')
            write_to_file(f, np.argmin(loss), 'loss', np.min(loss))
            write_to_file(f, np.argmin(loss_val), 'val_loss', np.min(loss_val))
            write_to_file(f, np.argmax(f1), 'f1', np.max(f1))
            write_to_file(f, np.argmax(f1_val), 'val_f1', np.max(f1_val))
            write_to_file(f, np.argmax(accuracy), 'accuracy', np.max(accuracy))
            write_to_file(f, np.argmax(accuracy_val), 'val_accuracy', np.max(accuracy_val))


def plot_data(data, title, save_path, y_label):
    for d in data:
        if any(np.isnan(x) for x in d):
            return
        if float('nan') in d:
            return
        plt.plot(d)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(save_path)
    plt.close()


def write_to_file(file, epoch, name, value):
    file.write('{},{},{}\n'.format(epoch, name, value))


if __name__ == '__main__':
    plot()